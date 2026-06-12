# Deployment Information

## Public URL
https://day12-ha-tang-cloud-va-deployment-i0sw.onrender.com

## Platform
Render

## Test Commands

### Health Check
```bash
curl https://day12-ha-tang-cloud-va-deployment-i0sw.onrender.com/health
# Expected: {"status": "ok", ...}
```

### API Test (with authentication)
```bash
curl -X POST https://day12-ha-tang-cloud-va-deployment-i0sw.onrender.com/ask \
  -H "X-API-Key: dev-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is stateless design?"}'
```

## Environment Variables Set
- ENVIRONMENT=production
- REDIS_URL=[Redacted]
- OPENAI_API_KEY=[Redacted]
- AGENT_API_KEY=[Redacted]
- RATE_LIMIT_PER_MINUTE=20
- DAILY_BUDGET_USD=5.0

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
