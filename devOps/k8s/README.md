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


### Urls

http://rabbitmq.flora.local.com/
http://app-api.flora.local.com/
http://grafana.flora.local.com/


## PVC with KinD
./kubectl apply -f https://git.io/pvc-test.yaml    
hostname > /pvc/hostname