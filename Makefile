DEFAULT_PROJECT_NAME=movies_ugc

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

CURRENT_ENVIRONMENT_PREFIX=PREFIX_DEV

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE=docker-compose.test.yml
DOCKER_COMPOSE_TEST_DEV_FILE=docker-compose.test.dev.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build
COMPOSE_PROFILE_DEFAULT=""--profile default""

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

# looking for docker-compose files
ifeq (,$(wildcard ./${DOCKER_COMPOSE_PROD_FILE}))
	DOCKER_COMPOSE_PROD_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_DEV_FILE}))
	DOCKER_COMPOSE_DEV_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_TEST_FILE}))
	DOCKER_COMPOSE_TEST_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_TEST_DEV_FILE}))
	DOCKER_COMPOSE_TEST_DEV_FILE=_
endif

# set envs if they are not defined
ifeq ($(COMPOSE_PROJECT_NAME),)
	COMPOSE_PROJECT_NAME=$(DEFAULT_PROJECT_NAME)
endif
ifeq ($(DOCKER_BUILDKIT),)
	DOCKER_BUILDKIT=1
endif
ifeq ($(ENVIRONMENT),)
	ENVIRONMENT=production
endif
ifeq ($(ENVIRONMENT), development)
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_DEV}
else
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_PROD}
endif


define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}$(strip ${1})${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef


define run_docker_compose_for_env
	@if [ $(strip ${2}) != "_" ]; then \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			override_file="-f ${2}" \
			cmd=$(strip ${3}); \
    else \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			cmd=$(strip ${3}); \
    fi
endef
run_docker_compose_for_env:
	@if [ $(strip ${env}) != "_" ]; then \
		DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
		COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME}_$(strip ${env}) \
		docker-compose \
			-f ${DOCKER_COMPOSE_MAIN_FILE} \
			$(strip ${override_file}) \
			$(strip ${cmd}); \
    else \
		DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
		COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
		docker-compose \
			-f ${DOCKER_COMPOSE_MAIN_FILE} \
			$(strip ${override_file}) \
			$(strip ${cmd}); \
    fi


define run_docker_compose_for_current_env
	@if [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_DEV} ]; then \
		if [ "${DOCKER_COMPOSE_DEV_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_DEV_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    elif [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_PROD} ]; then \
		if [ "${DOCKER_COMPOSE_PROD_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_PROD_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    fi
endef


# remove all existing containers, volumes, images
.PHONEY: remove
remove:
	@clear
	@echo "${RED}----------------!!! DANGER !!!----------------"
	@echo "Вы собираетесь удалить все неиспользуемые образы, контейнеры и тома."
	@echo "Будут удалены все незапущенные контейнеры, все образы для незапущенных контейнеров и все тома для незапущенных контейнеров"
	@read -p "${ORANGE}Вы точно уверены, что хотите продолжить? [yes/n]: ${RESET}" TAG \
	&& if [ "_$${TAG}" != "_yes" ]; then echo aborting; exit 1 ; fi
	docker-compose down --rmi all --volumes --remove-orphans && docker system prune -a --volumes --force



# stop and remove all running containers
.PHONEY: down down-prod down-dev down-test
down:
	$(call log, Down containers)
	@make down-prod
	@make down-dev
	@make down-test
down-prod:
	$(call run_docker_compose_for_env, "${PREFIX_PROD}", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
down-dev:
	$(call run_docker_compose_for_env, "${PREFIX_DEV}", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
down-test:
	$(call run_docker_compose_for_env, "${PREFIX_TEST}", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")


# build and run docker containers in demon mode
.PHONEY: run
run: down
	$(call log, Run containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile default ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# build and run docker containers in demon mode for oltp profile
.PHONEY: run-oltp
run-oltp: down
	$(call log, Run containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile oltp ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# build and run docker containers in demon mode for olap profile
.PHONEY: run-olap
run-olap: down
	$(call log, Run containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile olap ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# show container's logs
.PHONEY: logs _logs
logs:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _logs s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
_logs:
	$(call run_docker_compose_for_current_env, logs ${s})


# run bash into container
.PHONEY: bash _bash
bash:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _bash s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
_bash:
	$(call run_docker_compose_for_current_env, exec -it ${s} bash)


# stop containers
.PHONEY: stop _stop
stop:
	@read -p "${ORANGE}Containers name (press Enter to stop all containers): ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _stop s="$${_TAG}"; \
	else \
	    make _stop; \
	fi
_stop:
	$(call log, Stop containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, stop ${s})


# show docker-compose configuration
.PHONEY: config
config:
	$(call log, Docker-compose configuration (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, ${COMPOSE_PROFILE_DEFAULT} config)


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
