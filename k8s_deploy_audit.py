#!/usr/bin/env python3
"""
Kubernetes Deployment Audit CLI Tool
Author: Harish Gaddam
Role: DevSecOps Engineer Test Project – IntelliSense.io

Description:
  - Fetches deployment info (name, images, timestamp) from namespaces.
  - Compares two namespaces and reports differences.
  - Performs container, configuration, and network security checks.
  - Runs Trivy image vulnerability scans.
  - Exports a Markdown report for review.
"""

import argparse
import subprocess
# Use Kubernetes API
from kubernetes import client, config
from tabulate import tabulate
from datetime import datetime

# ------------------------
# Load kubeconfig
# ------------------------
def load_config():
    """Load Kubernetes config (from local or in-cluster)."""
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()


# ------------------------
# Get deployments info
# List deployments in a namespace
# ------------------------
def get_deployments(namespace):
    """Fetch deployments and metadata from a namespace."""
    apps = client.AppsV1Api()
    try:
        deployments = apps.list_namespaced_deployment(namespace=namespace).items
    except client.exceptions.ApiException as e:
        print(f" Could not list deployments in namespace '{namespace}': {e.reason}")
        return []

    result = []
    for d in deployments:
        
        # Display images of each deployment
        images = [c.image for c in d.spec.template.spec.containers]

        # Show date deployment was updated
        timestamp = (
            d.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if d.metadata.creation_timestamp
            else "N/A"
        )
        result.append({
            "name": d.metadata.name,
            "images": ", ".join(images),
            "timestamp": timestamp,
        })
    return result


# ------------------------
# Compare namespaces
# Compare two namespaces
# ------------------------
def compare_namespaces(ns1_data, ns2_data):
    """Compare deployment images between two namespaces."""
    ns1_map = {d["name"]: d["images"] for d in ns1_data}
    ns2_map = {d["name"]: d["images"] for d in ns2_data}
    all_deployments = sorted(set(ns1_map.keys()) | set(ns2_map.keys()))
    diff = []

    # Detect missing services
    for dep in all_deployments:
        img1 = ns1_map.get(dep, "MISSING")
        img2 = ns2_map.get(dep, "MISSING")
        if img1 != img2:
            diff.append([dep, img1, img2])

    return diff

# ------------------------
# Privileged Pod Security Check
# Container-level security check (privileged containers)
# ------------------------
def check_privileged_pods(namespace):
    """Check for privileged containers within a namespace."""
    v1 = client.CoreV1Api()
    risky = []
    try:
        pods = v1.list_namespaced_pod(namespace=namespace).items
        for pod in pods:
            for c in pod.spec.containers:
                sc = c.security_context
                if sc and getattr(sc, "privileged", False):
                    risky.append(f"Pod '{pod.metadata.name}' container '{c.name}' runs privileged=True.")
    except Exception as e:
        risky.append(f"Error checking privileged pods in {namespace}: {e}")
    return risky


# ------------------------
# Network policy presence
# Configuration-level checks (security context, non-root, resource limits)
# ------------------------
def extended_security_checks(namespace: str):
    """
    Perform extended container, configuration, and network security checks:
      - Ensures containers run as non-root
      - Checks for absence of securityContext
      - Checks for missing resource limits
      - Verifies NetworkPolicy existence
    """
    findings = []
    v1 = client.CoreV1Api()
    apps = client.AppsV1Api()
    net = client.NetworkingV1Api()

    # --- Pod Security Context Checks ---
    try:
        pods = v1.list_namespaced_pod(namespace=namespace).items
        for pod in pods:
            for c in pod.spec.containers:
                sc = c.security_context
                if sc is None:
                    findings.append(f"Pod '{pod.metadata.name}' container '{c.name}' has no securityContext defined.")
                elif getattr(sc, 'run_as_non_root', None) is not True:
                    findings.append(f"Pod '{pod.metadata.name}' container '{c.name}' is not set to runAsNonRoot=True.")
    except Exception as e:
        findings.append(f"Error checking pod security context in {namespace}: {e}")

    # --- Resource Limits Check ---
    try:
        deployments = apps.list_namespaced_deployment(namespace=namespace).items
        for d in deployments:
            for c in d.spec.template.spec.containers:
                res = c.resources
                if not res or not res.limits:
                    findings.append(f"Deployment '{d.metadata.name}' container '{c.name}' has no resource limits set.")
    except Exception as e:
        findings.append(f"Error checking resource limits in {namespace}: {e}")

    # --- Network Policy Check ---
    try:
        nps = net.list_namespaced_network_policy(namespace=namespace).items
        if not nps:
            findings.append(f"No NetworkPolicy found in namespace '{namespace}'.")
    except Exception as e:
        findings.append(f"Error checking NetworkPolicies in {namespace}: {e}")

    if not findings:
        findings.append("All extended security checks passed with no issues found.")
    return findings


# ------------------------
# Ingress TLS Verification
# Network-level checks (Ingress TLS)
# ------------------------
def check_ingress_tls(namespace: str):
    """Check for Ingress resources without TLS configuration."""
    findings = []
    net = client.NetworkingV1Api()
    try:
        ingresses = net.list_namespaced_ingress(namespace=namespace).items
        if not ingresses:
            findings.append(f"No Ingress resources found in namespace '{namespace}'.")
        for ing in ingresses:
            tls = getattr(ing.spec, "tls", None)
            if not tls:
                findings.append(f"Ingress '{ing.metadata.name}' has no TLS configuration (HTTP only).")
            else:
                findings.append(f"Ingress '{ing.metadata.name}' is secured with TLS")
    except Exception as e:
        findings.append(f"Error checking Ingress TLS in namespace '{namespace}': {e}")
    return findings


# ------------------------
# Trivy Vulnerability Scanning
# Vulnerability scanning of container images
# ------------------------
def scan_image_vulnerabilities(image_name: str, full_output=False):
    """
    Run Trivy scan on a container image and return vulnerability info.
    If full_output=True, include the full scan table output for report.md.
    """
    findings = []
    try:
        result = subprocess.run(
            ["trivy", "image", "--no-progress", "--severity", "CRITICAL,HIGH,MEDIUM,LOW", image_name],
            capture_output=True, text=True, timeout=180
        )

        if result.returncode == 0:
            findings.append(f"[{image_name}]  No CRITICAL/HIGH vulnerabilities found.\n")
        else:
            output = (result.stdout or result.stderr).strip()
            if full_output:
                findings.append(f"###  Full Trivy Scan Report for `{image_name}`\n")
                findings.append("```\n" + output + "\n```\n")
            else:
                # Summary mode (for terminal print)
                lines = output.splitlines()
                summary = "\n".join(lines[:20]) if len(lines) > 20 else output
                findings.append(f"[{image_name}]  Vulnerabilities detected:\n{summary}\n")
    except FileNotFoundError:
        findings.append(" Trivy not installed. Please install it using 'brew install trivy'.")
    except subprocess.TimeoutExpired:
        findings.append(f"[{image_name}] Scan timed out after 180s.")
    except Exception as e:
        findings.append(f"[{image_name}] Error during scan: {str(e)}")
    return findings



# ------------------------
# Markdown Report Generation
# ------------------------
def generate_markdown_report(ns1, ns2, ns1_data, ns2_data, diff, sec1, sec2, filename):
    """Generate a Markdown report summarising findings."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(f"# Kubernetes Deployment Audit Report\n")
    lines.append(f"**Generated on:** {now}\n")
    lines.append(f"**Namespaces Compared:** `{ns1}` vs `{ns2}`\n\n")

    lines.append(f"##  Deployments in {ns1}\n")
    lines.append(tabulate(ns1_data, headers='keys', tablefmt='github') if ns1_data else "No deployments found.")
    lines.append("\n\n")

    lines.append(f"##  Deployments in {ns2}\n")
    lines.append(tabulate(ns2_data, headers='keys', tablefmt='github') if ns2_data else "No deployments found.")
    lines.append("\n\n")

    # Highlight differences in images between namespaces
    lines.append(f"##  Differences Between Namespaces\n")
    if diff:
        lines.append(tabulate(diff, headers=["Deployment", ns1, ns2], tablefmt="github"))
    else:
        lines.append(" No differences found between the two namespaces.")
    lines.append("\n\n")

    lines.append(f"## Security Findings\n")
    if not sec1 and not sec2:
        lines.append(" No privileged containers detected.\n")
    else:
        if sec1:
            lines.append(f"### Namespace: {ns1}\n")
            lines += [f"- {issue}" for issue in sec1]
        if sec2:
            lines.append(f"\n### Namespace: {ns2}\n")
            lines += [f"- {issue}" for issue in sec2]

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    print(f"\n Markdown report saved as: {filename}")

# ------------------------
# Main Function
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="Kubernetes Deployment Audit Tool")
    parser.add_argument("--ns1", required=True, help="First namespace (e.g. nb-default)")
    parser.add_argument("--ns2", required=True, help="Second namespace (e.g. nb-modified)")
    parser.add_argument("--report", help="Output report file (e.g. report.md)")
    parser.add_argument("--skip-trivy", action="store_true", help="Skip Trivy image scanning (faster)")
    args = parser.parse_args()

    load_config()
    apps_v1 = client.AppsV1Api()

    # Gather deployment data
    ns1_data = get_deployments(args.ns1)
    ns2_data = get_deployments(args.ns2)

    print(f"\n=== Deployments in {args.ns1} ===")
    print(tabulate(ns1_data, headers="keys", tablefmt="github") if ns1_data else "No deployments found.")

    print(f"\n=== Deployments in {args.ns2} ===")
    print(tabulate(ns2_data, headers="keys", tablefmt="github") if ns2_data else "No deployments found.")

    # Highlight differences in images between namespaces
    # Compare namespaces
    print("\n=== Differences between namespaces ===")
    diff = compare_namespaces(ns1_data, ns2_data)
    if diff:
        print(tabulate(diff, headers=["Deployment", args.ns1, args.ns2], tablefmt="github"))
    else:
        print("No differences found!")

    # Basic security checks
    print("\n=== Privileged Container Security Checks ===")
    sec1 = check_privileged_pods(args.ns1)
    sec2 = check_privileged_pods(args.ns2)
    if not sec1 and not sec2:
        print("No privileged containers detected.")
    else:
        for issue in sec1 + sec2:
            print("-", issue)

    # Extended Security Checks
    print("\n=== Extended Security Checks ===")
    ext_sec_ns1 = extended_security_checks(args.ns1)
    ext_sec_ns2 = extended_security_checks(args.ns2)
    for f in ext_sec_ns1:
        print(f"[{args.ns1}] {f}")
    for f in ext_sec_ns2:
        print(f"[{args.ns2}] {f}")

    # Ingress TLS Checks
    print("\n=== Ingress TLS Verification ===")
    tls_findings_ns1 = check_ingress_tls(args.ns1)
    tls_findings_ns2 = check_ingress_tls(args.ns2)
    for f in tls_findings_ns1:
        print(f"[{args.ns1}] {f}")
    for f in tls_findings_ns2:
        print(f"[{args.ns2}] {f}")

    # Container Image Vulnerability Scans
    unique_images = set()
    for ns in [args.ns1, args.ns2]:
        try:
            deployments = apps_v1.list_namespaced_deployment(namespace=ns).items
            for d in deployments:
                for c in d.spec.template.spec.containers:
                    unique_images.add(c.image)
        except Exception as e:
            print(f" Error fetching deployments for {ns}: {e}")

    if not args.skip_trivy:
        print("\n=== Image Vulnerability Scans (Trivy) ===")
        for img in sorted(unique_images):
            results = scan_image_vulnerabilities(img)
            for r in results:
                print(r)
    else:
        print("\n=== Image Vulnerability Scans skipped (--skip-trivy) ===")

    # Generate Markdown report
    if args.report:
        generate_markdown_report(args.ns1, args.ns2, ns1_data, ns2_data, diff, sec1, sec2, args.report)
        try:
            with open(args.report, "a") as f:
                f.write("\n\n### Extended Security Checks\n")
                for fnd in ext_sec_ns1 + ext_sec_ns2:
                    f.write(f"- {fnd}\n")
                f.write("\n\n### Ingress TLS Verification\n")
                for fnd in tls_findings_ns1 + tls_findings_ns2:
                    f.write(f"- {fnd}\n")
                f.write("\n\n### Image Vulnerability Scans (Trivy)\n")
                for img in sorted(unique_images):
                    f.write(f"\n\n##  Trivy Vulnerability Report for `{img}`\n")
                    if args.skip_trivy:
                        f.write(" Trivy scan skipped (--skip-trivy used)\n")
                    else:
                        scan_results = scan_image_vulnerabilities(img, full_output=True)
                        for res in scan_results:
                            f.write(res + "\n")

        except Exception as e:
            print(f" Could not append extra results to report file: {e}")

    print("\n Audit completed successfully.")


if __name__ == "__main__":
    main()
