# Kubernetes Deployment CLI Tool

## 1. Project Overview

This tool audits deployments running on Kubernetes clusters to identify version differences, configuration inconsistencies, and potential security issues.

## Key Features
It provides tabular and Markdown reports.
* Deployment Audit: Lists all deployments within a namespace, including:
    Deployment name
    Container images
    Last updated timestamp
* Namespace Comparison:
    Highlights differences in deployments between two namespaces (e.g., missing services or version mismatches).
* Security Scanning:
    Detects privileged or non-root containers.
    Checks for missing resource limits and absent securityContext.
    Validates presence of Network Policies.
    Verifies Ingress TLS configuration.
    Performs image vulnerability scans using Trivy.
* Comprehensive Reporting:
    Generates a structured report.md with findings and recommendations.

---

## 2. Prerequisites

Ensure the following tools are installed and accessible from your terminal:

| Tool            | Purpose                         | Installation Command (MacOS)                        |
| --------------- | ------------------------------- | --------------------------------------------------- |
| **Python 3.9+** | Run the audit tool              | Pre-installed on macOS or via `brew install python` |
| **pip**         | Python package manager          | Included with Python                                |
| **kubectl**     | Manage Kubernetes clusters      | `brew install kubectl`                              |
| **Minikube**    | Local Kubernetes cluster        | `brew install minikube`                             |
| **Docker**      | Run containers                  | Install Docker Desktop                              |
| **Trivy**       | Container vulnerability scanner | `brew install trivy`                                |

---

## 3. Environment Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/harishg99/k8s-deploy-cli-tool
cd k8s-deploy-audit
```

### Step 2: Set up and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Kubernetes Cluster Setup

### Step 1: Start Minikube

```bash
minikube start
```

### Step 2: Deploy the Online Boutique sample application

```bash
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
cd microservices-demo/release
kubectl create namespace nb-default
kubectl apply -f kubernetes-manifests.yaml -n nb-default
```

### Step 3: Duplicate the deployment into another namespace

```bash
kubectl create namespace nb-modified
kubectl apply -f kubernetes-manifests.yaml -n nb-modified
```

---

## 5. Modify the Second Namespace for Comparison

### Step 1: Update the frontend image version in `nb-modified`

```bash
kubectl set image deployment/frontend frontend=gcr.io/google-samples/microservices-demo/frontend:v0.2.0 -n nb-modified
```

This ensures the two namespaces differ, demonstrating version drift.

---

## 6. Ingress Configuration (for TLS Verification)

### Step 1: Create an ingress without TLS in `nb-default`

Create the file `ingress-no-tls.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: nb-default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: frontend.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

Apply the ingress:

```bash
kubectl apply -f ingress-no-tls.yaml
```

Verify:

```bash
kubectl get ingress -n nb-default
```

Expected output:

```
NAME               CLASS    HOSTS            ADDRESS   PORTS   AGE
frontend-ingress   <none>   frontend.local             80      1m
```

### Step 2: Create a TLS-enabled ingress in `nb-modified`

#### Generate a self-signed TLS certificate

```bash
mkdir tls && cd tls
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -out tls.crt -keyout tls.key -subj "/CN=frontend.local/O=frontend.local"
```

#### Create a Kubernetes TLS secret

```bash
kubectl create secret tls tls-secret \
  --cert=tls.crt \
  --key=tls.key \
  -n nb-modified
```

Verify the secret:

```bash
kubectl get secrets -n nb-modified
```

Expected output:

```
NAME          TYPE                DATA   AGE
tls-secret    kubernetes.io/tls   2      1m
```

#### Create the TLS ingress YAML (`ingress-tls.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: nb-modified
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
      - frontend.local
    secretName: tls-secret
  rules:
  - host: frontend.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

Apply and verify:

```bash
kubectl apply -f ingress-tls.yaml
kubectl get ingress -n nb-modified
```

Expected output:

```
NAME               CLASS    HOSTS            ADDRESS   PORTS     AGE
frontend-ingress   <none>   frontend.local             80, 443   1m
```

---

## 7. Run the Audit Tool

From the root of your project directory:

```bash
python k8s_deploy_audit.py --ns1 nb-default --ns2 nb-modified --report report.md
```

This command:

* Compares both namespaces
* Performs all security and network checks
* Scans container images for vulnerabilities using Trivy
* Generates a comprehensive Markdown report (`report.md`)

---

## 8. Expected Report Output

Your `report.md` file will include:

* All deployments (name, image, timestamp)
* Namespace differences (missing or mismatched services)
* Container security checks
* Configuration checks (non-root, missing limits)
* Network security checks (NetworkPolicy presence)
* Ingress TLS verification (shows both HTTP and HTTPS)
* Trivy vulnerability summary per image

Example excerpt:

```
### Ingress TLS Verification
- Ingress 'frontend-ingress' has no TLS configuration (HTTP only).
- Ingress 'frontend-ingress' is secured with TLS
```

---

## 9. Cleanup

To delete all resources and free cluster space:

```bash
kubectl delete namespace nb-default nb-modified
minikube stop
```

---

## 10. Notes

* The Online Boutique demo does not include Ingress resources by default; these were manually added to validate the network and TLS security checks.
* The tool can be reused on any Kubernetes cluster by updating namespace names and report file paths.

---

## 11. Project Validation Summary

| Requirement                               | Description                       | Status    |
| ----------------------------------------- | --------------------------------- | --------- |
| List deployments (name, image, timestamp) | Uses Kubernetes API               | Completed |
| Compare two namespaces                    | Identifies differences            | Completed |
| Security checks                           | Privileged pods, non-root, limits | Completed |
| Network checks                            | NetworkPolicy presence            | Completed |
| Ingress checks                            | TLS vs non-TLS detection          | Completed |
| Vulnerability scanning                    | Trivy integrated                  | Completed |
| Report generation                         | Markdown output                   | Completed |
| GitHub repository                         | Publicly accessible               | Completed |

