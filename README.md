# Installation Instructions

## macOS (Homebrew)

```bash
# Install kubectl and Minikube
brew install kubectl minikube

# Start Minikube with the Docker driver
minikube start --driver=docker
# minikube start --cpus=4 --memory=4096 --driver=docker

```

## Linux (Debian / Ubuntu)

```bash
# Download and install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Download and install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start --driver=docker
# minikube start --cpus=4 --memory=4096 --driver=docker
```

## Windows (Chocolatey or PowerShell)

```powershell
# Using Chocolatey
choco install kubernetes-cli minikube

# Start Minikube using Docker Desktop or Hyper-V
minikube start --driver=docker
# minikube start --cpus=4 --memory=4096 --driver=docker
```

## Some usefull commands

```bash

# Starts cluster with specified k8s version
minikube start --kubernetes-version=v1.28.0

# Start a cluster with 3 nodes (1 master, 2 workers)
minikube start --nodes 3 -p multinode-demo

# Add a new worker node to the active cluster
minikube node add -p multinode-demo

# Add a specific node type (e.g., an additional control plane for High Availability)
minikube node add --control-plane -p multinode-demo

# Remove a specific node from the cluster
minikube node delete multinode-demo-m02 -p multinode-demo

# Delete the existing profile or already created cluster
minikube delete 
```

## Install Docker

### macOS

```bash
# Install Docker Desktop
# Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/

# Verify installation
docker --version
```

### Linux (Ubuntu / Debian)

```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start and enable Docker
sudo systemctl enable docker
sudo systemctl start docker

# Verify installation
docker --version
```

### Windows

```powershell
# Install Docker Desktop from https://www.docker.com/products/docker-desktop/
# Or use Docker Engine with WSL2

docker --version
```

## Install podman

### macOS

```bash
# Install Podman
brew install podman

# Verify installation
podman --version
```

## Build Images Directly inside Minikube (Docker)

```bash
# Point local Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build v1 image
docker build -t demo-fastapik8s:v1 .

# In case of error with build or docker context or buildx issues
minikube image build -t demo-fastapik8s:v1 .

# Incase above fails Check for 
docker buildx ls 
docker context ls
unset DOCKER_HOST # after the eval command is executed for the minikube docker-env which sets the env variables

# Build v2 image (pass APP_VERSION env during runtime or build)
docker build -t demo-fastapik8s:v2 .

# In case of error with build or docker context or buildx issues
minikube image build -t demo-fastapik8s:v2 .
```

## Alternative: Use Podman to Build Container Images

Podman can be used as an alternative to Docker for building container images when Docker is not installed or preferred.

### Install Podman

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
# Use Podman Desktop or a compatible podman setup on Windows
podman --version
```

### Build an image with Podman

```bash
# Build the image with Podman
podman build -t demo-fastapi:v1 .

# Optional: run locally for testing
podman run --rm -p 8000:8000 demo-fastapi:v1
```

> Note: If you use Podman instead of Docker, you may need to push or load the image into Minikube using a compatible method, depending on your environment.

## Enable Istio Addon / CLI

```bash
# Download Istio (1.x)
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Install the Istio demo profile on Minikube
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

## Deploy the FastAPI App to Minikube

```bash
# Ensure Minikube is running
minikube status

# Apply Kubernetes manifests
kubectl apply -f k8s/replicaset.yaml
kubectl apply -f k8s/pod.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# get objects
kubectl get rs
kubectl get deploy
kubectl get pods
kubectl get svc

# Scaling
kubectl scale deployments/fastapi-demo --replicas=3
```

## Test the Application

```bash
# Port-forward the service to your local machine
kubectl port-forward service/fastapik8s-demo 8000:80
OR
minikube service fastapik8s-demo --url
# with the output ip and port you can call the service. Because you are using a Docker driver on darwin, the terminal needs to be open to run it.

# In another terminal, test the endpoints
curl http://localhost:8000/
curl http://localhost:8000/healthz
```

Example response:

```json
{"status":"healthy","version":"v1.0.0","message":"Hello from FastAPI on K8s!"}
```

## Useful Minikube Commands

```bash
# Start Minikube
minikube start

# Minikube profile. Shows its driver, container runtime, status, # of nodes
minikube profile list

# Open the Kubernetes dashboard
minikube dashboard

# Open the Kubernetes dashboard with url
minikube dashboard --url

# List Default Addons / Plugins
minikube addons list

# Enable Addons / Plugins
minikube addons enable csi-hostpath-driver

# Instal non avialble addons using Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install downloaded AddOns as namespace eg monitoring stack here
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace



# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```