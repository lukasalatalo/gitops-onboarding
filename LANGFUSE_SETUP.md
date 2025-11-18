# Langfuse Integration Setup Guide

Langfuse has been integrated into your infrastructure for LLM observability and tracing. This guide will help you complete the setup.

## What Was Added

1. **Langfuse PostgreSQL Database** - Separate database for Langfuse data
2. **Langfuse Deployment** - Main Langfuse application
3. **Langfuse Service** - Internal service for Langfuse
4. **Langfuse Ingress** - External access to Langfuse UI (optional)
5. **LiteLLM Integration** - Updated LiteLLM to send traces to Langfuse

## Setup Steps

### 1. Generate Secure Secrets

Before deploying, generate secure values for Langfuse secrets:

```bash
# Generate NEXTAUTH_SECRET
openssl rand -base64 32

# Generate SALT
openssl rand -base64 32
```

Update `langfuse/deployment.yaml` with these values:
- Replace `change-this-to-a-secure-random-string` for `NEXTAUTH_SECRET`
- Replace `change-this-to-a-secure-random-string` for `SALT`

### 2. Deploy Langfuse

Deploy all resources:

```bash
kubectl apply -k .
```

Wait for Langfuse to be ready:

```bash
kubectl wait --for=condition=available --timeout=300s deployment/langfuse
```

### 3. Access Langfuse UI and Get API Keys

Port-forward to Langfuse:

```bash
kubectl port-forward svc/langfuse 3000:3000
```

Open your browser and go to: `http://localhost:3000`

1. **Create an account** - First user becomes admin
2. **Go to Settings → API Keys**
3. **Create a new API key** (or use the default one)
4. **Copy the Secret Key** (starts with `lf-sk-`)
5. **Copy the Public Key** (starts with `lf-pk-`)

### 4. Update LiteLLM with Langfuse API Keys

Update `litellm/deployment.yaml` with the actual API keys:

```yaml
- name: LANGFUSE_SECRET_KEY
  value: "lf-sk-your-actual-secret-key"  # Replace with actual key
- name: LANGFUSE_PUBLIC_KEY
  value: "lf-pk-your-actual-public-key"  # Replace with actual key
```

Apply the updated deployment:

```bash
kubectl apply -k .
kubectl rollout restart deployment/litellm
```

### 5. Verify Integration

1. Make some requests through OpenWebUI
2. Check Langfuse UI at `http://localhost:3000` (via port-forward)
3. You should see traces appearing in the Langfuse dashboard

## Accessing Langfuse

### Option 1: Port-Forward (Development)

```bash
kubectl port-forward svc/langfuse 3000:3000
# Access at http://localhost:3000
```

### Option 2: Ingress (Production)

Update `langfuse/ingress.yaml` with your domain:

```yaml
- host: langfuse.yourdomain.com  # Replace with your domain
```

Then access via: `https://langfuse.yourdomain.com`

## What Langfuse Tracks

With this integration, Langfuse will automatically track:

- **All LLM requests** made through LiteLLM
- **Model usage** and costs
- **Latency** and performance metrics
- **Token usage** per request
- **Request/response** data
- **Errors** and failures

## Troubleshooting

### Langfuse not receiving traces?

1. Check LiteLLM logs:
   ```bash
   kubectl logs deployment/litellm
   ```

2. Verify API keys are correct in LiteLLM deployment

3. Check Langfuse connectivity:
   ```bash
   kubectl exec -it deployment/litellm -- curl http://langfuse:3000/api/public/health
   ```

### Langfuse pod not starting?

1. Check pod status:
   ```bash
   kubectl get pods -l app=langfuse
   kubectl describe pod -l app=langfuse
   ```

2. Check database connection:
   ```bash
   kubectl logs deployment/langfuse
   ```

3. Verify PostgreSQL is running:
   ```bash
   kubectl get pods -l app=langfuse-postgres
   ```

## Security Notes

⚠️ **Important**: Before deploying to production:

1. Change all default passwords in secrets
2. Use secure random strings for `NEXTAUTH_SECRET` and `SALT`
3. Consider using Kubernetes Secrets for sensitive values instead of plain text
4. Use PersistentVolumeClaims for PostgreSQL data persistence
5. Enable TLS/SSL for Langfuse ingress
6. Set up proper authentication/authorization

## Next Steps

- Configure Langfuse projects and environments
- Set up alerts and monitoring
- Integrate with other observability tools
- Configure data retention policies

