# Deployment Information

## Public URL
https://day12-agent-production.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://day12-agent-production.railway.app/health
# Expected: {"status": "ok", ...}
```

### API Test (with authentication)
```bash
curl -X POST https://day12-agent-production.railway.app/ask \
  -H "X-API-Key: my-production-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is stateless design?"}'
```

## Environment Variables Set
- PORT=8000
- REDIS_URL=redis://localhost:6379
- AGENT_API_KEY=my-production-secret-key
- LOG_LEVEL=INFO
- RATE_LIMIT_PER_MINUTE=10
- MONTHLY_BUDGET_USD=10.0

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
