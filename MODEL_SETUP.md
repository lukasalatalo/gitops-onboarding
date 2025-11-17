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

**Step 1: Verify LiteLLM has models**
```bash
# Port-forward to LiteLLM
kubectl port-forward svc/litellm 4000:4000

# In another terminal, check models
curl -H "Authorization: Bearer dummy" http://localhost:4000/v1/models
```

If this returns an empty list or error, **you need to add models first** via the dashboard (Option 1) or API (Option 2).

**Step 2: Verify OpenWebUI can reach LiteLLM**
```bash
# Test from OpenWebUI pod
kubectl exec -it deployment/openwebui -- wget -qO- http://litellm:4000/v1/models
```

**Step 3: Check OpenWebUI connection in UI**
Even with environment variables set, you may need to configure the connection in OpenWebUI UI:

1. Port-forward to OpenWebUI:
   ```bash
   kubectl port-forward svc/openwebui 8080:8080
   ```

2. Open `http://localhost:8080` in browser

3. Go to **Settings** → **Connections** (or **Admin Panel** → **Connections**)

4. Create/verify connection:
   - **URL:** `http://litellm:4000` (or `http://litellm:4000/v1` - try both)
   - **Key:** `dummy`

5. Save and refresh the page

**Step 4: Check logs**
```bash
# LiteLLM logs
kubectl logs deployment/litellm --tail=50

# OpenWebUI logs
kubectl logs deployment/openwebui --tail=50 | grep -i model
```

**Step 5: Restart services**
```bash
kubectl rollout restart deployment/openwebui
kubectl rollout restart deployment/litellm
```

**Step 6: Run automated troubleshooting**
```bash
./troubleshoot-models.sh
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

