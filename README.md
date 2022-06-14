## Asynchronous Ubereats restaurants web crawler built with Django, Celery, Redis, Docker, BeautifulSoup and Requests

Django web server using Celery server to handle asynchronous tasks by using Redis as a message Broker

- [Install](#install)
  * [Docker-compose install](#docker-compose-install)
- [Execute](#execute)
  + [Run tasks](#run-tasks)

Components:
* Web Framework [Django](https://www.djangoproject.com/)
* Database [PostgreSQL](https://www.postgresql.org)
* Task Queue [Celery](https://docs.celeryproject.org/en/stable/)
* Message Broker and Cache [Redis](https://redis.io/)

### Install

---

Types of installation

1. [Docker-compose](#docker-compose-install)

#### Docker-compose install

Uses the default Django development server.

1. Rename *.env.example* to *.env*.
2. Update the environment variables in the *.env* file.
3. Prepare Django environment to start up

```bash
$ make makemigrations
$ make migrate
$ make createsuperuser
$ make collectstatic
```

4. Build the images and run the containers:

```bash
$ make up-development
```
Test it out at [http://localhost:8000](http://localhost:8000).

### Execute

---

#### Run Tasks

1. run tasks manually from the shell:

```shell
$ docker-compose -f docker-compose.dev.yml exec appserver python manage.py shell
$ from crawlers.location.tasks import start_location_task
$ start_location_task.delay()
```

2. How to stop all pending tasks:

```shell
$ docker-compose -f docker-compose.dev.yml exec appserver python manage.py shell
$ from appserver.celery import app
$ app.control.purge()
```