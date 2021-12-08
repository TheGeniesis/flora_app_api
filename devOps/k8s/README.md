# A KIND with playground

## Quick Information

- Simple stack with monitoring/logging

## Requirements

- [Docker](https://www.docker.com/)
- [Docker-compose](https://docs.docker.com/compose/)
- [Task](https://taskfile.dev)
- [envrc](https://direnv.net/)

## Setup

- task install
- task rebuild
> If it fails run `task deploy:k8s`

### Grafana Dashboards

```bash
task forward:grafana
# Open in browser http://localhost:3000
# credentials admin/12tsh3
```