# novalex-api

---
## Requirements

- docker
- docker-compose

---

## Local development
### docker compose
Application is ready for local development with docker compose

### Run

To start the project in develop mode, run the following command:

```bash
make start
```

or just

```bash
make
```

To check if everything is OK:

```bash
curl http://localhost:8002/api/v1/status
```

To stop working and docker containers:

```bash
make stop
```

To clean up work of docker containers and images:

```bash
make clean
```

### Testing

```bash
make run-test
```

### All available commands

```bash
make help
```

## Software

- python3.12
