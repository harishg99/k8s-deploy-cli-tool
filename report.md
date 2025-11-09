# Kubernetes Deployment Audit Report

**Generated on:** 2025-11-09 20:16:44

**Namespaces Compared:** `nb-default` vs `nb-modified`


##  Deployments in nb-default

| name                  | images                                                                                     | timestamp           |
|-----------------------|--------------------------------------------------------------------------------------------|---------------------|
| adservice             | us-central1-docker.pkg.dev/google-samples/microservices-demo/adservice:v0.10.3             | 2025-11-09 12:43:45 |
| cartservice           | us-central1-docker.pkg.dev/google-samples/microservices-demo/cartservice:v0.10.3           | 2025-11-09 12:43:45 |
| checkoutservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/checkoutservice:v0.10.3       | 2025-11-09 12:43:45 |
| currencyservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/currencyservice:v0.10.3       | 2025-11-09 12:43:45 |
| emailservice          | us-central1-docker.pkg.dev/google-samples/microservices-demo/emailservice:v0.10.3          | 2025-11-09 12:43:45 |
| frontend              | us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3              | 2025-11-09 12:43:45 |
| loadgenerator         | us-central1-docker.pkg.dev/google-samples/microservices-demo/loadgenerator:v0.10.3         | 2025-11-09 12:43:45 |
| paymentservice        | us-central1-docker.pkg.dev/google-samples/microservices-demo/paymentservice:v0.10.3        | 2025-11-09 12:43:45 |
| productcatalogservice | us-central1-docker.pkg.dev/google-samples/microservices-demo/productcatalogservice:v0.10.3 | 2025-11-09 12:43:45 |
| recommendationservice | us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3 | 2025-11-09 12:43:45 |
| redis-cart            | redis:alpine                                                                               | 2025-11-09 12:43:45 |
| shippingservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/shippingservice:v0.10.3       | 2025-11-09 12:43:45 |



##  Deployments in nb-modified

| name                  | images                                                                                     | timestamp           |
|-----------------------|--------------------------------------------------------------------------------------------|---------------------|
| adservice             | us-central1-docker.pkg.dev/google-samples/microservices-demo/adservice:v0.10.3             | 2025-11-09 12:46:02 |
| checkoutservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/checkoutservice:v0.10.3       | 2025-11-09 12:46:02 |
| currencyservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/currencyservice:v0.10.3       | 2025-11-09 12:46:02 |
| emailservice          | us-central1-docker.pkg.dev/google-samples/microservices-demo/emailservice:v0.10.3          | 2025-11-09 12:46:02 |
| frontend              | gcr.io/google-samples/microservices-demo/frontend:v0.2.0                                   | 2025-11-09 12:46:02 |
| loadgenerator         | us-central1-docker.pkg.dev/google-samples/microservices-demo/loadgenerator:v0.10.3         | 2025-11-09 12:46:02 |
| paymentservice        | us-central1-docker.pkg.dev/google-samples/microservices-demo/paymentservice:v0.10.3        | 2025-11-09 12:46:02 |
| productcatalogservice | us-central1-docker.pkg.dev/google-samples/microservices-demo/productcatalogservice:v0.10.3 | 2025-11-09 12:46:02 |
| recommendationservice | us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3 | 2025-11-09 12:46:02 |
| redis-cart            | redis:alpine                                                                               | 2025-11-09 12:46:02 |
| shippingservice       | us-central1-docker.pkg.dev/google-samples/microservices-demo/shippingservice:v0.10.3       | 2025-11-09 12:46:02 |



##  Differences Between Namespaces

| Deployment   | nb-default                                                                       | nb-modified                                              |
|--------------|----------------------------------------------------------------------------------|----------------------------------------------------------|
| cartservice  | us-central1-docker.pkg.dev/google-samples/microservices-demo/cartservice:v0.10.3 | MISSING                                                  |
| frontend     | us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3    | gcr.io/google-samples/microservices-demo/frontend:v0.2.0 |



## Security Findings

 No privileged containers detected.


### Extended Security Checks
- Pod 'adservice-dbd9db68f-tz77z' container 'server' is not set to runAsNonRoot=True.
- Pod 'cartservice-7d446cd6cd-m4pgm' container 'server' is not set to runAsNonRoot=True.
- Pod 'checkoutservice-b45957b77-9kpgh' container 'server' is not set to runAsNonRoot=True.
- Pod 'currencyservice-768c464f5-qk85j' container 'server' is not set to runAsNonRoot=True.
- Pod 'emailservice-5756ddcbb5-xmwt5' container 'server' is not set to runAsNonRoot=True.
- Pod 'frontend-6d47d98676-mskc6' container 'server' is not set to runAsNonRoot=True.
- Pod 'loadgenerator-645dcc4d68-g7p27' container 'main' is not set to runAsNonRoot=True.
- Pod 'paymentservice-69c9f447bf-gthkh' container 'server' is not set to runAsNonRoot=True.
- Pod 'productcatalogservice-66db9f456f-5g2lj' container 'server' is not set to runAsNonRoot=True.
- Pod 'recommendationservice-5767cf4d97-47z6z' container 'server' is not set to runAsNonRoot=True.
- Pod 'redis-cart-c8ff86559-h7r8j' container 'redis' is not set to runAsNonRoot=True.
- Pod 'shippingservice-7c44749569-zc542' container 'server' is not set to runAsNonRoot=True.
- No NetworkPolicy found in namespace 'nb-default'.
- Pod 'adservice-dbd9db68f-4gdss' container 'server' is not set to runAsNonRoot=True.
- Pod 'checkoutservice-b45957b77-9n2dj' container 'server' is not set to runAsNonRoot=True.
- Pod 'currencyservice-768c464f5-sqcqg' container 'server' is not set to runAsNonRoot=True.
- Pod 'emailservice-5756ddcbb5-llj9t' container 'server' is not set to runAsNonRoot=True.
- Pod 'frontend-87b87f465-z5d92' container 'server' is not set to runAsNonRoot=True.
- Pod 'loadgenerator-645dcc4d68-mb9dn' container 'main' is not set to runAsNonRoot=True.
- Pod 'paymentservice-69c9f447bf-njc52' container 'server' is not set to runAsNonRoot=True.
- Pod 'productcatalogservice-66db9f456f-6lgcx' container 'server' is not set to runAsNonRoot=True.
- Pod 'recommendationservice-5767cf4d97-qp7r6' container 'server' is not set to runAsNonRoot=True.
- Pod 'redis-cart-c8ff86559-qbhvj' container 'redis' is not set to runAsNonRoot=True.
- Pod 'shippingservice-7c44749569-vwswj' container 'server' is not set to runAsNonRoot=True.
- No NetworkPolicy found in namespace 'nb-modified'.


### Ingress TLS Verification
- Ingress 'frontend-ingress' has no TLS configuration (HTTP only).
- Ingress 'frontend-ingress' is secured with TLS


### Image Vulnerability Scans (Trivy)


  Trivy Vulnerability Report for `gcr.io/google-samples/microservices-demo/frontend:v0.2.0`

#  Trivy Vulnerability Report for `gcr.io/google-samples/microservices-demo/frontend:v0.2.0`

[gcr.io/google-samples/microservices-demo/frontend:v0.2.0]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `redis:alpine`

#  Trivy Vulnerability Report for `redis:alpine`

[redis:alpine]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/adservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/adservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/adservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/cartservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/cartservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/cartservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/checkoutservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/checkoutservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/checkoutservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/currencyservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/currencyservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/currencyservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/emailservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/emailservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/emailservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/loadgenerator:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/loadgenerator:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/loadgenerator:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/paymentservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/paymentservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/paymentservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/productcatalogservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/productcatalogservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/productcatalogservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.


  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/shippingservice:v0.10.3`

#  Trivy Vulnerability Report for `us-central1-docker.pkg.dev/google-samples/microservices-demo/shippingservice:v0.10.3`

[us-central1-docker.pkg.dev/google-samples/microservices-demo/shippingservice:v0.10.3]  No CRITICAL/HIGH vulnerabilities found.

