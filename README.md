
# Minikube Setup with Helm and Docker

## Prerequisites
Ensure the following are installed and configured:

- **Minikube** with Docker CLI enabled.
- **Ingress Controller** enabled on Minikube.

## Steps

### 1. Create a Dockerfile
Create a `Dockerfile` in your project directory.

### 2. Build a Docker Image
Run the following command to build the Docker image:
```bash
docker build -t <image_name>:<tag> .
```

### 3. Create a Helm Chart
Create a new Helm chart by running:
```bash
helm create <chart-name>
```

### 4. Modify Helm Files
Update the following files to fit your application’s needs:
- **Deployment** (under `templates/deployment.yaml`)
- **Ingress** (under `templates/ingress.yaml`)
- **Services** (under `templates/service.yaml`)
- **Values** (under `values.yaml`)

### 5. Deploy the Application Using Helm
Use Helm to deploy the Docker image with the following commands:

1. Check the list of deployed applications:
   ```bash
   helm list
   ```

2. Install the application:
   ```bash
   helm install <app_name> .
   ```

3. Uninstall the application:
   ```bash
   helm uninstall <app_name>
   ```

---

## Ingress Controller Configuration

To adjust the Ingress Controller's configuration, use the following steps:

1. Get the Ingress ConfigMap:
   ```bash
   kubectl get configmap -n ingress-nginx
   ```

2. View the full configuration of the Ingress Controller:
   ```bash
   kubectl get configmap ingress-nginx-controller -n ingress-nginx -o yaml
   ```

3. Edit the ConfigMap:
   ```bash
   kubectl edit configmap ingress-nginx-controller -n ingress-nginx
   ```

4. Restart the Ingress Controller to apply changes:
   ```bash
   kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
   ```

### Configuration Options for File Size and Buffering:
To modify file size and buffering settings, you can add the following configuration values to the ConfigMap:

```yaml
client-body-timeout: 60s
client-max-body-size: 64m
proxy-body-size: 64m
server-tokens: "false"
use-forwarded-headers: "true"
```

---

## Useful Kubernetes Commands

### General Commands for Minikube
- Get the list of all pods:
  ```bash
  kubectl get pods
  ```

- Get the list of all services:
  ```bash
  kubectl get svc
  ```

- Get detailed services information:
  ```bash
  kubectl get services
  ```

### Commands for Viewing Logs
- Get logs of a specific pod:
  ```bash
  kubectl logs <pod-name> -n <namespace>
  ```

- Get logs of a specific container inside a pod:
  ```bash
  kubectl logs <pod-name> -c <container-name> -n <namespace>
  ```

- View previous logs (after a restart):
  ```bash
  kubectl logs <pod-name> --previous -n <namespace>
  ```

- Get logs of all pods in a deployment:
  ```bash
  kubectl logs -l app=<label> -n <namespace>
  ```

---

## Summary of Log Commands

1. **Single pod logs**: 
   ```bash
   kubectl logs <pod-name> -n <namespace>
   ```

2. **Follow logs** (real-time):
   ```bash
   kubectl logs -f <pod-name> -n <namespace>
   ```

3. **Logs for a specific container**:
   ```bash
   kubectl logs <pod-name> -c <container-name> -n <namespace>
   ```

4. **Previous logs** (after restart):
   ```bash
   kubectl logs <pod-name> --previous -n <namespace>
   ```

5. **Logs from all pods in a deployment**:
   ```bash
   kubectl logs -l app=<label> -n <namespace>
   ```
