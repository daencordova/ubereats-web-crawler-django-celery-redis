DOCKER_DEV_FILE = docker-compose -f docker-compose.dev.yml
DOCKER_PROD_FILE = docker-compose -f docker-compose.prod.yml

up-development:
	${DOCKER_DEV_FILE} up --build

down-development:
	${DOCKER_DEV_FILE} down

up-production:
	${DOCKER_PROD_FILE} up --build

down-production:
	${DOCKER_PROD_FILE} down

makemigrations:
	python app/manage.py makemigrations

migrate:
	python app/manage.py migrate

createsuperuser:
	python app/manage.py createsuperuser

collectstatic:
	python app/manage.py collectstatic --no-input --clear 