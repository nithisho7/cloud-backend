# Cloud Backend API + Flask + AWS EC2 + DOCKER

## Overview

Flask-based REST API with authentication and CRUD operations, deployed on AWS EC2 using Docker and Nginx, with CI/CD via GitHub Actions.

## Stack

* Flask (Python)
* Docker
* Nginx
* AWS EC2
* GitHub Actions
* SQLite
* JWT Auth

## Features

* JWT authentication
* CRUD for items
* Protected routes
* Health check endpoint
* CI/CD auto-deploy

## API

| Method | Endpoint   |
| ------ | ---------- |
| GET    | /health    |
| POST   | /login     |
| GET    | /items     |
| POST   | /items     |
| PUT    | /items/:id |
| DELETE | /items/:id |

## Run Locally

```bash
git clone <your-repo-url>
cd cloud-backend
docker-compose up --build
```

## Deployment

* Dockerized app on EC2
* Nginx reverse proxy (port 80 → 5000)
* GitHub Actions handles deploy on push


## CI/CD

Push → GitHub Actions → SSH EC2 → pull → rebuild → restart container

IT Student | Cloud / DevOps
