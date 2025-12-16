# sovereign-ai

This repo contains code and notes for my tests with self-hosting LLMs.

## Running with docker compose

```bash
docker network create common_network
docker compose -f docker-compose.vllm.yml up -d
docker compose -f docker-compose.monitoring.yml up -d
```

## Architecture

The setup now supports running components independently:
- **vLLM**: Runs on `localhost:8000`
- **Prometheus**: Runs on `localhost:9090` 
- **Grafana**: Runs on `localhost:3000`

This separation allows you to manage vLLM without needing to restart the monitoring stack.
