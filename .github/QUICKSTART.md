# GitHub Actions Deployment - Quick Start

## 🚀 Deploy with Latest Tag (Main Branch)

```bash
# Make your changes
git add .
git commit -m "feat: add new feature"
git push origin main

# ✅ Triggers: jocosta96/soat-challenge:latest deployment
```

## 🏷️ Deploy with Specific Tag

```bash
# Create and push a tag
git tag v1.2.3
git push origin v1.2.3

# ✅ Triggers: jocosta96/soat-challenge:v1.2.3 deployment
```

## 🔐 Required GitHub Secrets

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKER_USERNAME` | Docker Hub username | `your-username` |
| `DOCKER_PAT` | Docker Hub Personal Access Token | `your-personal-access-token` |
| `KUBE_CONFIG_DATA` | Base64 kubeconfig | `cat ~/.kube/config \| base64 -w 0` |

## ⚡ Quick Commands

```bash
# Setup secrets help
./.github/scripts/setup-secrets.sh

# Validate deployment
./.github/scripts/validate-deployment.sh

# Update manifests manually
./.github/scripts/update-manifests.sh v1.2.3

# Check deployment status
kubectl get pods -l app=dpm-app
kubectl get hpa
kubectl logs -f deployment/dpm-app
```

## 🎯 What Happens When You Deploy

### Main Branch Push → Latest Tag
1. **Build** `jocosta96/soat-challenge:latest` image
2. **Push** to Docker Hub
3. **Update** Kubernetes manifests
4. **Deploy** to cluster with rolling update
5. **Verify** health checks and scaling

### Tag Creation → Specific Tag  
1. **Build** `jocosta96/soat-challenge:v1.2.3` image
2. **Push** to Docker Hub  
3. **Update** Kubernetes manifests
4. **Deploy** to cluster with rolling update
5. **Verify** health checks and scaling

## 📊 Monitor Your Deployment

```bash
# Watch GitHub Actions
# Go to: https://github.com/your-repo/actions

# Monitor Kubernetes
kubectl get pods -w
kubectl get hpa -w

# Check health endpoints
kubectl port-forward service/svc-app-nodeport 8080:80
curl http://localhost:8080/health
curl http://localhost:8080/docs
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker login failed | Check `DOCKER_USERNAME` and `DOCKER_PAT` |
| Kubernetes access denied | Verify `KUBE_CONFIG_DATA` secret |
| Pod startup timeout | Check resource limits and health checks |
| Image pull failed | Ensure image was pushed successfully |

## 🔗 Links

- **Full Documentation**: [DEPLOYMENT.md](.github/DEPLOYMENT.md)
- **Setup Guide**: Run `.github/scripts/setup-secrets.sh`
- **Validation Script**: `.github/scripts/validate-deployment.sh`
- **Workflow File**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

---

**🎯 Ready to deploy? Just push to main or create a tag!**
