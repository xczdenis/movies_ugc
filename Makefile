DEFAULT_PROJECT_NAME=movies_ugc

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE=docker-compose.test.yml
DOCKER_COMPOSE_TEST_DEV_FILE=docker-compose.test.dev.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build


# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell printf "\033[30m")
	RED          := $(shell printf "\033[91m")
	GREEN        := $(shell printf "\033[92m")
	YELLOW       := $(shell printf "\033[33m")
	BLUE         := $(shell printf "\033[94m")
	PURPLE       := $(shell printf "\033[95m")
	ORANGE       := $(shell printf "\033[93m")
	WHITE        := $(shell printf "\033[97m")
	RESET        := $(shell printf "\033[00m")
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	ORANGE       := ""
	WHITE        := ""
	RESET        := ""
endif


# read env variables from .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif


# set COMPOSE_PROJECT_NAME if it is not defined
ifeq ($(COMPOSE_PROJECT_NAME),)
	COMPOSE_PROJECT_NAME=$(DEFAULT_PROJECT_NAME)
endif

ifeq ($(DOCKER_BUILDKIT),)
	DOCKER_BUILDKIT=1
endif


define run_docker_compose
	DOCKER_BUILDKIT=$(DOCKER_BUILDKIT) COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME)_$(1) docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(2) $(3) $(4)
endef


define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}$(1)${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef


#down: $(RUN_PROD_DOWN) $(RUN_DEV_DOWN) $(RUN_TEST_DOWN)
#	$(call log,Down containers $(COMPOSE_PROJECT_NAME))
#	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_PROD_FILE) down
#	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_DEV_FILE) down
#	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_TEST_FILE) down
down: dev-down
	$(call log, Down containers $(COMPOSE_PROJECT_NAME))
	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) down

remove:
	@clear
	@echo "${RED}----------------!!! DANGER !!!----------------"
	@echo "Вы собираетесь удалить все неиспользуемые образы, контейнеры и тома."
	@echo "Будут удалены все незапущенные контейнеры, все образы для незапущенных контейнеров и все тома для незапущенных контейнеров"
	@read -p "${ORANGE}Вы точно уверены, что хотите продолжить? [yes/n]: ${RESET}" TAG \
	&& if [ "_$${TAG}" != "_yes" ]; then echo aborting; exit 1 ; fi
	docker system prune -a -f --volumes


#############
# PROD
#############
prod: down
	$(call log,Run containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


prod-check:
	$(call log,Check configuration (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),config)


prod-stop:
	$(call log,Stop running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),stop,$(s))


prod-down:
	$(call log,Down running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),down)


prod-logs:
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),logs,$(s))


#############
# DEV
#############
dev: down
	$(call log,Run containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


dev-check:
	$(call log,Check configuration (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),config)


dev-stop:
	$(call log,Stop running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


dev-down:
	$(call log,Down running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)


dev-logs:
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),logs,$(s))


fake:
	@clear
	@echo "${RED}----------------!!! DANGER !!!----------------"
	@echo "${PURPLE}Будет выполнено копирование файла ${WHITE}.env.template${PURPLE} в ${WHITE}.env.${PURPLE}"
	@echo "Если файл ${WHITE}.env${PURPLE} уже существует, то он будет перезеписан."
	@echo "А потом сразу запустится разворачивание кластера и замеры производительности."
	@read -p "${BLUE}Вы точно уверены, что хотите продолжить? [yes/n]: ${RESET}" TAG \
	&& if [ "_$${TAG}" != "_yes" ]; then echo aborting; exit 1 ; fi
	@cp .env.template .env
	@make dev
	@chmod -R 777 ./scripts
	$(call log,"Запускаю инициализацию базы данных")
	@CH_LOCAL_MODE=true python src/db_upgrade.py
	$(call log,"Запускаю загрузку данных")
	python src/load_data.py


ch-db-upgrade-local:
	@CH_LOCAL_MODE=true python src/db_upgrade.py
