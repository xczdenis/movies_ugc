# UGC-movies

UGC-movies - сервис генерации контента для [Онлайн кинотеатра "Movies"](https://github.com/xczdenis/movies).

Сервис предоставляет возможность обрабатывать огромное количество данных, генерируемых пользователями
онлайн-кинотеатра. Например, данные о поведении пользователя во время просмотра фильма. Также это могут быть
лайки, добавление в избранное, оценка фильма и т.д. На основании этих данных можно строить рекомендательную
систему.

Благодаря [Kafka](https://kafka.apache.org/), сервис способен обрабатывать огромное количество запросов в
секунду. Данные хранятся в [ClickHouse](https://clickhouse.tech/) - OLAP хранилище, это позволяет мгновенно
выполнять сложные аналитические запросы. Данные о лайках и избранном хранятся в
[MongoDB](https://www.mongodb.com/), что позволяет быстро выполнять запросы к данным и масштабировать
хранилище горизонтально без предела.


## Особенности

<ul>
<li>Работает с <b>Python 3.11</b>;</li>
<li>Полностью асинхронный;</li>
<li><b>ClickHouse кластер</b> - OLAP хранилище. Легко настраиваемый конфиг кластера;</li>
<li><b>Kafka кластер</b> - обработка потоковых данных:</li>
<ul>
    <li><b>aiokafka</b> - асинхронная работа с kafka;</li>
    <li><b>schema_registry</b> - централизованное хранилище и валидация схем kafka;</li>
    <li><b>kafka-ui</b> - веб-интерфейс для кластера kafka;</li>
</ul>
<li><b>Непрерывный ETL</b> процесс из Kafka в ClickHouse</li>
<li><b>MongoDB кластер</b> - отказоустойчивый, масштабируемый кластер для хранение данных о лайках и избранном;</li>
<li><b>FastAPI</b> - быстрый и современный фреймворк для создания API;</li>
<li><b>Nginx</b> - веб-сервер для обработки запросов к API;</li>
<li><b>Python инитеры</b> - python-код для автоматической инициализации всех кластеров:</li>
<ul>
    <li>Clickhouse initer;</li>
    <li>Kafka initer;</li>
    <li>Mongo initer;</li>
</ul>
<li>Полная интеграция с <b>Docker</b>:</li>
<ul>
    <li>Docker-compose для локальной разработки;</li>
    <li>Тесты в Docker;</li>
    <li>Тонкие образы, благодаря multi-stage сборке;</li>
</ul>
<li><b>Makefile</b> - удобный интерфейс для запуска команд проекта;</li>
<li><b>Pre-commit hooks</b> - автоматическая проверка кода перед коммитом для соблюдения стандартов разработки;</li>
<li><b>Conventional commits</b> - стандарт для написания коммитов;</li>
<li>Применение <b>SOLID принципов</b>.</li>
</ul>


## Функционал сервиса

Сервис предоставляет следующий функционал:
1. Фиксация события, произошедшего во время просмотра фильма (начало просмотра, пауза, перемотка вперед,
назад, остановка);
2. Фиксация текущей позиции воспроизведения фильма;
3. Добавление общего времени просмотра фильма для построения рекомендательной системы;
4. Добавление фильма в избранное. Получение списка избранных фильмов;
5. Оценки фильмов.

Подробную документацию API можно посмотреть по адресу: [http://127.0.0.1:8000/api/v1/openapi/](http://127.0.0.1:8000/api/v1/openapi#/)
![openapi.png](docs/assets/img/openapi.png)


## Чистая архитектура
Сервис построен на основе принципов чистой архитектуры. Бизнес-логика оперирует абстракциями и отделена
от конкретных реализации, например, базы данных.

Например, рассмотрим, процесс добавления данных о времени, потраченном пользователем на просмотр
фильма. Диаграмма последовательности процесса представлена ниже:

![add_movie_viewing_uml.png](docs/assets/img/add_movie_viewing_uml.png)
![img.png](img.png)
Разберем участников процесса:
1. `Controller` - ендпоинт, обрабатывающий запрос от клиента;
2. `MovieViewingService` - выполняет бизнес логику;
3. `MovieViewingGateway` - шлюз данных. Это интерфейс, предоставляющий методы работы с базой данных.
Весь код на языке запросов для конкретной базы данных должен находиться здесь;
4. `KafkaMovieViewingGateway` - конкретная реализация шлюза `MovieViewingGateway` для Kafka;
5. `DatabaseClient` - интерфейс, предоставляющий соединение с базой данных. Здесь присутствует метод `execute`,
который отправляет в базу данных запрос подготовленный в шлюзе `MovieViewingGateway`;
6. `KafkaEventProducerClient` - конкретная реализация интерфейса `DatabaseClient` для Kafka;


```python
@router.post(
    "/movie-viewing",
    name=make_rout_name(NAMESPACE, "add_movie_viewing"),
    response_description="The movie viewing time added successfully",
)
async def add_movie_viewing(
    request_movie_viewing: MovieViewingRequest,
    service: MovieViewingService = Depends(get_movie_viewing_service),
) -> MovieViewing:
    """
    Add time spent watching a movie.
    """
    movie_viewing = MovieViewing(
        user=User(id=request_movie_viewing.user_id),
        movie=Movie(id=request_movie_viewing.movie_id),
        viewed_seconds=request_movie_viewing.viewed_seconds,
    )

    await service.add_movie_viewing(movie_viewing=movie_viewing)

    return movie_viewing
```

## Requirements

* Python 3.11+
* Docker version 23.0.5+
* Docker Compose version 2.17.3+


## Быстрый старт

Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта, если иное не
указано в описании конкретной команды.


### Настройка переменных окружения

Создай файлы `.env` и `.env.local` в корне проекта, выполнив команду:
```bash
make env
```
Можно просто скопировать файлы `env.template` и `env.local.template`.


### Запуск проекта

🚨 Убедись, что у тебя свободны все следующие порты:
1. Все порты в `.env.local`;
2. Все порты раздела `Expose ports for clickhouse's nodes` в `.env`;
3. Порт `KAFKA_BROKER_EXPOSE_PORT` в `.env`.

🚨 Укажи свою платформу для docker образов в `.env`. Например, для Mac на M1 вот так:
```bash
DOCKER_IMG_PLATFORM=linux/arm64
```

Запустить проект:
```bash
make run
```

