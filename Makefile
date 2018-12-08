run:
	docker-compose -f docker/docker-compose.yml up
build:
	docker-compose -f docker/docker-compose.yml build
web:
	docker exec -it web bash
mongo:
	docker exec -it mongo mongo admin -u root -p
down:
	docker-compose -f docker/docker-compose.yml down -v
reset:
	docker stop $(docker ps -q); docker rm $(docker ps -a -q)
prune:
	docker volume prune -f
kill:
	make down; make reset; make prune; make run