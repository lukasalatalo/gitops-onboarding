# How to Add Models to LiteLLM for Open WebUI

With `STORE_MODEL_IN_DB: "true"`, you have three options to add models:

## Option 1: Use LiteLLM Dashboard (Easiest) ⭐ Recommended

1. **Port-forward to access LiteLLM UI:**
   ```bash
   kubectl port-forward svc/litellm 4000:4000
   ```

2. **Open browser:**
   - Go to: `http://localhost:4000/ui`
   - Login with password: `admin` (or whatever you set in `UI_PASSWORD`)

3. **Add models:**
   - Navigate to "Models" section
   - Click "Add Model" or "New Model"
   - Enter model details:
     - Model Name: `custom-model-1`
     - Model: `claude-latest`
     - API Base: `https://llm-proxy.edgez.live/v1`
     - API Key: `sk-K2AyiqHTpNHDp3vhmpChjQ`

4. **Verify:**
   - Models should appear in Open WebUI after a few seconds
   - Check: `curl http://localhost:4000/v1/models` (after port-forward)

## Option 2: Use LiteLLM API (Programmatic)

Add models via API calls:

```bash
# Port-forward first
kubectl port-forward svc/litellm 4000:4000

# Add a model
curl -X POST "http://localhost:4000/v1/model/new" \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "custom-model-1",
    "litellm_params": {
      "model": "claude-latest",
      "api_base": "https://llm-proxy.edgez.live/v1",
      "api_key": "sk-K2AyiqHTpNHDp3vhmpChjQ"
    }
  }'

# Verify models are available
curl http://localhost:4000/v1/models
```

## Option 3: Use Config File Only (Disable DB Storage)

If you prefer config file only, you can disable database storage:

1. **Update `litellm/deployment.yaml`:**
   - Change `STORE_MODEL_IN_DB: "true"` to `STORE_MODEL_IN_DB: "false"`
   - Or remove the environment variable entirely

2. **Models in `litellm/config.yaml` will be automatically loaded**

3. **Restart LiteLLM pod:**
   ```bash
   kubectl rollout restart deployment/litellm
   ```

## Troubleshooting

### Models not showing in Open WebUI?

1. **Verify LiteLLM has the models:**
   ```bash
   kubectl port-forward svc/litellm 4000:4000
   curl http://localhost:4000/v1/models
   ```

2. **Check LiteLLM logs:**
   ```bash
   kubectl logs deployment/litellm
   ```

3. **Verify Open WebUI connection:**
   - Check that `OPENAI_API_BASE` in OpenWebUI points to `http://litellm:4000/v1`
   - Check that `OPENAI_API_KEY` matches `LITELLM_MASTER_KEY` (both should be "dummy")

4. **Restart Open WebUI:**
   ```bash
   kubectl rollout restart deployment/openwebui
   ```

### Quick Test

Test if a model works directly:
```bash
kubectl port-forward svc/litellm 4000:4000

curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "custom-model-1",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

