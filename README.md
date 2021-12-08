# Flora app api

API for flora backend server


## Pre-requirements

- Dotenv
- Task
- Docker
- Python 3.8

## Installation

Run `task` command to see possibilities

### First run

- For Ubuntu (only supported) exec `task install:venv` to install venv app
- Create a new venv and install basic software `task init`

### Start application

- Login into a venv (command to run is generated by `task start:env`)
- Execute `task start`

## Links

- [RabbitMQ UI](http://localhost:15672/)
- [Swagger doc](http://localhost:8001/api/ui)

## Improvements

- Add possibility to send signal to start watering
- Add endpoint to force watering
- Add notification when water level is too low