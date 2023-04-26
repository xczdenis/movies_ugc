# UGC-movies


Сервис генерации контента для [Онлайн кинотеатра Movies](https://github.com/xczdenis/movies)

<hr>

**Исходный код**: [https://github.com/xczdenis/movies_ugc](https://github.com/xczdenis/movies_ugc)

**Документация**: [https://xczdenis.github.io/auth_movies](https://xczdenis.github.io/auth_movies/)

<hr>


## Функционал сервиса
UGC-сервис - это инструмент веб-аналитики, который предоставляет возможность обрабатывать и хранить данные,
генерируемые пользователями онлайн-кинотеатра. Например, это могут быть данные о просмотре фильма, которые
обновляются ежесекундно в онлайн режиме. На основании этих данных можно строить рекомендательную систему.

Основные функции:
1. OLAP хранилище;
2. Потоковый ввод данных.


## Используемые технологии
1. **ClickHouse** - OLAP хранилище;
2. **Kafka** - обработка потоковых данных;
- **aiokafka** - асинхронная работа с kafka;
- **schema_registry** - валидация схем kafka
- **kafka-ui** - веб-интерфейс для кластера kafka
3. **FastAPI** - приложение, реализующее API;
4. **Nginx** - веб-сервер.


## Requirements
* Python 3.11+
* Docker 20.10.17+


## Быстрый старт
Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта,
если иное не указано в описании конкретной команды.

!!! note
    В этом разделе описан процесс быстрого запуска проекта. Более подробную информацию о работе с сервисом
    смотри в разделах данного руководства.

### Настройка переменных окружения
Создай файл `.env` в корне проекта, скопировав шаблон `env.template`.

!!! warning
    Ты можешь ничего не менять в файле `.env`. В этом случае убедись, что у тебя свободны порты, указанные
    в следующих переменных:

    * все порты раздела `Expose ports for clickhouse's nodes`
    * `KAFKA_BROKER_EXPOSE_PORT`
    * `KAFKA_SCHEMA_REGISTRY_EXPOSE_PORT`
    * `KAFKA_UI_EXPOSE_PORT`

### Запуск проекта
Если у тебя доступно выполнение команд с помощью `make`, то смотри команду на вкладке `Make`.
Иначе смотри команду на вкладке `Native`.

Запустить проект в режиме:
=== "Make"

    <div class="termy">

    ```console
    $ make run

    ---> 100%
    Creating movies_auth-dev_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth-dev_jaeger_1   ... <span style="color: green;">done</span>
    Creating movies_auth-dev_redis_1    ... <span style="color: green;">done</span>
    Creating movies_auth-dev_app_1      ... <span style="color: green;">done</span>
    Creating movies_auth-dev_nginx_1    ... <span style="color: green;">done</span>

     ⠿ Network movies_ugc_dev_default                                  <span style="color: green;">Created</span>                                                                                                    0.0s
     ⠿ Container movies_ugc_dev-clickhouse-shard2-1                    <span style="color: green;">Healthy</span>                                                                                                    7.6s
     ⠿ Container movies_ugc_dev-clickhouse-default-node-1              <span style="color: green;">Started</span>                                                                                                    0.7s
     ⠿ Container movies_ugc_dev-clickhouse-default-node-with-keeper-1  <span style="color: green;">Started</span>                                                                                                    0.8s
     ⠿ Container movies_ugc_dev-clickhouse-shard1-1                    <span style="color: green;">Healthy</span>                                                                                                    7.6s
     ⠿ Container movies_ugc_dev-kafka-broker-1                         <span style="color: green;">Healthy</span>                                                                                                    7.0s
     ⠿ Container movies_ugc_dev-clickhouse-keeper-quorum-1             <span style="color: green;">Healthy</span>                                                                                                    7.5s
     ⠿ Container movies_ugc_dev-kafka-schema-registry-1                <span style="color: green;">Healthy</span>                                                                                                   12.9s
     ⠿ Container movies_ugc_dev-kafka-ui-1                             <span style="color: green;">Started</span>                                                                                                    6.4s
     ⠿ Container movies_ugc_dev-clickhouse-shard2-replica1-1           <span style="color: green;">Healthy</span>                                                                                                   12.5s
     ⠿ Container movies_ugc_dev-clickhouse-shard1-replica1-1           <span style="color: green;">Healthy</span>                                                                                                   12.5s
     ⠿ Container movies_ugc_dev-kafka-initer-1                         <span style="color: green;">Started</span>                                                                                                   13.2s
     ⠿ Container movies_ugc_dev-app-1                                  <span style="color: green;">Started</span>                                                                                                   13.3s
     ⠿ Container movies_ugc_dev-clickhouse-initer-1                    <span style="color: green;">Started</span>
    ```

    </div>

=== "Native"

    <div class="termy">

    ```console
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile default up -d --build

    ---> 100%
    Creating movies_auth-dev_postgres_1 ... <span style="color: green;">done</span>
    Creating movies_auth-dev_jaeger_1   ... <span style="color: green;">done</span>
    Creating movies_auth-dev_redis_1    ... <span style="color: green;">done</span>
    Creating movies_auth-dev_app_1      ... <span style="color: green;">done</span>
    Creating movies_auth-dev_nginx_1    ... <span style="color: green;">done</span>

     ⠿ Network movies_ugc_dev_default                                  <span style="color: green;">Created</span>                                                                                                    0.0s
     ⠿ Container movies_ugc_dev-clickhouse-shard2-1                    <span style="color: green;">Healthy</span>                                                                                                    7.6s
     ⠿ Container movies_ugc_dev-clickhouse-default-node-1              <span style="color: green;">Started</span>                                                                                                    0.7s
     ⠿ Container movies_ugc_dev-clickhouse-default-node-with-keeper-1  <span style="color: green;">Started</span>                                                                                                    0.8s
     ⠿ Container movies_ugc_dev-clickhouse-shard1-1                    <span style="color: green;">Healthy</span>                                                                                                    7.6s
     ⠿ Container movies_ugc_dev-kafka-broker-1                         <span style="color: green;">Healthy</span>                                                                                                    7.0s
     ⠿ Container movies_ugc_dev-clickhouse-keeper-quorum-1             <span style="color: green;">Healthy</span>                                                                                                    7.5s
     ⠿ Container movies_ugc_dev-kafka-schema-registry-1                <span style="color: green;">Healthy</span>                                                                                                   12.9s
     ⠿ Container movies_ugc_dev-kafka-ui-1                             <span style="color: green;">Started</span>                                                                                                    6.4s
     ⠿ Container movies_ugc_dev-clickhouse-shard2-replica1-1           <span style="color: green;">Healthy</span>                                                                                                   12.5s
     ⠿ Container movies_ugc_dev-clickhouse-shard1-replica1-1           <span style="color: green;">Healthy</span>                                                                                                   12.5s
     ⠿ Container movies_ugc_dev-kafka-initer-1                         <span style="color: green;">Started</span>                                                                                                   13.2s
     ⠿ Container movies_ugc_dev-app-1                                  <span style="color: green;">Started</span>                                                                                                   13.3s
     ⠿ Container movies_ugc_dev-clickhouse-initer-1                    <span style="color: green;">Started</span>
    ```

    </div>
