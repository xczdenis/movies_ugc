DEFAULT_PROJECT_NAME=movies_auth

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

PREFIX_CHECK=check
PREFIX_STOP=stop
PREFIX_DOWN=down
PREFIX_LOGS=logs

RUN_PROD=$(PREFIX_PROD)
RUN_PROD_CHECK=$(PREFIX_PROD)-$(PREFIX_CHECK)
RUN_PROD_STOP=$(PREFIX_PROD)-$(PREFIX_STOP)
RUN_PROD_DOWN=$(PREFIX_PROD)-$(PREFIX_DOWN)
RUN_PROD_LOGS=$(PREFIX_PROD)-$(PREFIX_LOGS)

RUN_DEV=$(PREFIX_DEV)
RUN_DEV_CHECK=$(PREFIX_DEV)-$(PREFIX_CHECK)
RUN_DEV_STOP=$(PREFIX_DEV)-$(PREFIX_STOP)
RUN_DEV_DOWN=$(PREFIX_DEV)-$(PREFIX_DOWN)
RUN_DEV_LOGS=$(PREFIX_DEV)-$(PREFIX_LOGS)

RUN_TEST=$(PREFIX_TEST)
RUN_TEST_CHECK=$(PREFIX_TEST)-$(PREFIX_CHECK)
RUN_TEST_STOP=$(PREFIX_TEST)-$(PREFIX_STOP)
RUN_TEST_DOWN=$(PREFIX_TEST)-$(PREFIX_DOWN)
RUN_TEST_LOGS=$(PREFIX_TEST)-$(PREFIX_LOGS)

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
	DOCKER_BUILDKIT=0
endif


define run_docker_compose
	DOCKER_BUILDKIT=$(DOCKER_BUILDKIT) COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME)_$(1) docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(2) $(3) $(4)
endef


define run_docker_compose_pure
	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) $(1)
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
down: $(RUN_DEV_DOWN)
	$(call log,Down containers $(COMPOSE_PROJECT_NAME))
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
$(RUN_PROD): down
	$(call log,Run containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_PROD_CHECK):
	$(call log,Check configuration (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),config)


$(RUN_PROD_STOP):
	$(call log,Stop running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),stop,$(s))


$(RUN_PROD_DOWN):
	$(call log,Down running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),down)


$(RUN_PROD_LOGS):
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),logs,$(s))


#############
# DEV
#############
$(RUN_DEV): down
	$(call log,Run containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_DEV_CHECK):
	$(call log,Check configuration (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),config)


$(RUN_DEV_STOP):
	$(call log,Stop running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


$(RUN_DEV_DOWN):
	$(call log,Down running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)


$(RUN_DEV_LOGS):
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
	$(call log,"Жду пока кластер развернется")
	@sleep 4
	$(call log,"Запускаю инициализацию базы данных")
	python src/init_db.py
	$(call log,"Запускаю загрузку данных")
	python src/load_data.py

