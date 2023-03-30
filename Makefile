mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

all:

frontend-dev:
	cd $(mkfile_dir)/frontend; npm run dev;

backend-dev:
	cd $(mkfile_dir)/backend; uvicorn main:app --reload;

# Build Docker Images
build-frontend:
	docker build --network=host -t registry.gitlab.com/maomaocake/smart-farm/frontend $(mkfile_dir)/frontend

build-backend:
	docker build --network=host -t registry.gitlab.com/maomaocake/smart-farm/backend $(mkfile_dir)/backend

build-frontend-no-cache:
	docker build --no-cache --network=host -t registry.gitlab.com/maomaocake/smart-farm/frontend $(mkfile_dir)/frontend

build-backend-no-cache:
	docker build --no-cache --network=host -t registry.gitlab.com/maomaocake/smart-farm/backend $(mkfile_dir)/backend

build-backend-worker-no-cache:
	docker build --no-cache --network=host -t registry.gitlab.com/maomaocake/smart-farm/backend-worker $(mkfile_dir)/backend-worker

build-docker:build-frontend-no-cache build-backend-no-cache build-backend-worker-no-cache


# Docker Commands
push-dockers:
	docker push registry.gitlab.com/maomaocake/smart-farm/frontend:latest
	docker push registry.gitlab.com/maomaocake/smart-farm/backend:latest
	docker push registry.gitlab.com/maomaocake/smart-farm/backend-worker:latest


run-frontend:
	 docker run -it --rm -d -p 3000:3000 --name frontend registry.gitlab.com/maomaocake/smart-farm/frontend

run-backend:
	 docker run -it --rm -d -p 8000:8000 --name backend registry.gitlab.com/maomaocake/smart-farm/backend

run-all-docker:
	docker-compose up -d

stop-all-docker:
	docker-compose down