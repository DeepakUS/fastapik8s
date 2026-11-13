# FastAPI on Kubernetes Setup

This project contains a FastAPI application and Kubernetes manifests. The steps below are organized by phase so it is easier to install dependencies, start Minikube, build images, deploy the app, and validate the service.

---

## Phase 1: Installation

### 1.1 Install Docker

#### macOS

```bash
# Install Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

docker --version
```

#### Linux (Ubuntu / Debian)

```bash
sudo apt-get update
sudo apt-get install -y docker.io

sudo systemctl enable docker
sudo systemctl start docker

docker --version
```

#### Windows

```powershell
# Install Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

# Or use Docker Engine with WSL2

docker --version
```

### 1.2 Install Minikube and kubectl

#### macOS (Homebrew)

```bash
brew install kubectl minikube
kubectl version --client
minikube version
```

#### Linux (Debian / Ubuntu)

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

kubectl version --client
minikube version
```

#### Windows (Chocolatey or PowerShell)

```powershell
# Using Chocolatey
choco install kubernetes-cli minikube

kubectl version --client
minikube version
```

### 1.3 Install Podman

#### macOS

```bash
brew install podman
podman --version
```

#### Linux (Ubuntu / Debian)

```bash
sudo apt-get update
sudo apt-get install -y podman
podman --version
```

#### Windows

```powershell
# Use Podman Desktop or a compatible Podman setup
podman --version
```

---

## Phase 2: Minikube Startup and Cluster Setup

### 2.1 Start Minikube

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# Optional: custom resources
# minikube start --cpus=4 --memory=4096 --driver=docker
```

### 2.2 Useful Minikube commands

```bash
# Start with a specific Kubernetes version
minikube start --kubernetes-version=v1.28.0

# Start a cluster with 3 nodes
minikube start --nodes 3 -p multinode-demo

# Add a new node
minikube node add -p multinode-demo

# Add a control-plane node for HA
minikube node add --control-plane -p multinode-demo

# Remove a node
minikube node delete multinode-demo-m02 -p multinode-demo

# Check cluster status
minikube status

# Open the dashboard
minikube dashboard

# Open dashboard URL only
minikube dashboard --url

# List profiles
minikube profile list

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

### 2.3 Verify cluster readiness

```bash
kubectl get nodes
kubectl get pods -A
kubectl cluster-info
```

### 2.4 Optional: enable add-ons

```bash
minikube addons list
minikube addons enable csi-hostpath-driver
```

### 2.5 Optional: install Istio

```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

---

## Phase 3: Build Phase

### 3.1 Build image with Docker

```bash
# Point Docker CLI to Minikube Docker daemon
eval $(minikube docker-env)

# Build the image
docker build -t demo-fastapik8s:v1 .

# If Docker build issues occur, try Minikube's direct image build
minikube image build -t demo-fastapik8s:v1 .

# Useful troubleshooting
# docker buildx ls
# docker context ls
# unset DOCKER_HOST

# Build a second version as needed
docker build -t demo-fastapik8s:v2 .
minikube image build -t demo-fastapik8s:v2 .
```

### 3.2 Build image with Podman

```bash
# Build the image with Podman
podman build -t demo-fastapi:v1 .

# Optional local run for quick verification
podman run --rm -p 8000:8000 demo-fastapi:v1
```

> Note: If using Podman instead of Docker, you may need to load or push the image into Minikube depending on your runtime environment.

---

## Phase 4: Deployment Phase

### 4.1 Apply Kubernetes manifests

```bash
# Ensure Minikube is running
minikube status

# Apply the app resources
kubectl apply -f k8s/pod.yaml
kubectl apply -f k8s/replicaset.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4.2 Check deployed resources

```bash
kubectl get rs
kubectl get deploy
kubectl get pods
kubectl get svc
```

### 4.3 Scale the deployment

```bash
kubectl scale deployments/fastapi-demo --replicas=3
kubectl get pods
```

---

## Phase 5: Testing Phase

### 5.1 Expose the service locally

```bash
# Port-forward the service
kubectl port-forward service/fastapik8s-demo 8000:80
```

Or use Minikube service URL:

```bash
minikube service fastapik8s-demo --url
```

### 5.2 Test the API endpoints

Open a second terminal and run:

```bash
curl http://localhost:8000/
curl http://localhost:8000/healthz
```

Example response:

```json
{"status":"healthy","version":"v1.0.0","message":"Hello from FastAPI on K8s!"}
```

### 5.3 Useful validation commands

```bash
kubectl get pods -w
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

---

## Quick Start Summary

```bash
# 1. Install required tools
brew install kubectl minikube docker

# 2. Start Minikube
minikube start --driver=docker

# 3. Build the app image
eval $(minikube docker-env)
docker build -t demo-fastapik8s:v1 .

# 4. Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 5. Test the app
kubectl port-forward service/fastapik8s-demo 8000:80
curl http://localhost:8000/healthz
```

This phased flow keeps installation, cluster setup, image build, deployment, and validation separate so that each stage is easy to follow and troubleshoot.