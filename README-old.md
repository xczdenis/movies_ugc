# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.

Задания на спринт вы найдёте внутри тем.


## ClickHouse

### Параметры кластера
* Количество шардов: 2
* Количество реплик: по 2 на шард
* Итого серверов: 4

### Загрузка в БД
Всего строк: 25000096

| Размер пачки | Общее время    | Только SQL     | Всего пачек | Время вставки пачки, с | Post обработка                              |
|--------------|----------------|----------------|-------------|------------------------|---------------------------------------------|
| 1k           | 0:01:30.998547 | 0:00:53.804383 | 25.025      | 00.002                 | еще что-то происходит в течении 10-15 минут |
| 10k          | 0:00:48.829842 | 0:00:14.851207 | 2500        | 00.006                 | -                                           |
| 100k         | 0:00:43.696801 | 0:00:09.995806 | 250         | 00.04                  | -                                           |
| 1m           | 0:00:42.482256 | 0:00:09.867204 | 25          | 00.4                   | -                                           |
| 10m          | 0:00:42.225571 | 0:00:07.929844 | 2           | 4.01                   | -                                           |

### Чтение из БД
```sql
SELECT movie_id, COUNT(*) movie_count FROM views_progress GROUP BY movie_id ORDER BY movie_count DESC LIMIT 20
20 rows retrieved starting from 1 in 108 ms (execution: 74 ms, fetching: 34 ms)
```

```sql
SELECT COUNT(*) FROM (SELECT movie_id, COUNT(*) movie_count FROM views_progress GROUP BY movie_id) as view_movie_counter WHERE movie_count<10
1 row retrieved starting from 1 in 113 ms (execution: 77 ms, fetching: 36 ms)
```

```sql
SELECT movie_id, sum(movie_frame) as sum_movie_frame FROM views_progress GROUP BY movie_id ORDER BY sum_movie_frame DESC LIMIT 20
20 rows retrieved starting from 1 in 142 ms (execution: 103 ms, fetching: 39 ms)
```

```sql
SELECT user_id, count(*) as movies_count FROM (SELECT DISTINCT user_id, movie_id FROM views_progress GROUP BY user_id, movie_id) as view_user_movie GROUP BY user_id ORDER BY movies_count DESC LIMIT 20
20 rows retrieved starting from 1 in 1 s 567 ms (execution: 1 s 562 ms, fetching: 5 ms)
```

```sql
SELECT user_id, SUM(max_user_movie_frame) as total_user_movies_frame FROM (SELECT DISTINCT user_id, movie_id, MAX(movie_frame) as max_user_movie_frame FROM views_progress GROUP BY user_id, movie_id) as view_user_movie GROUP BY user_id ORDER BY total_user_movies_frame DESC LIMIT 20
20 rows retrieved starting from 1 in 2 s 387 ms (execution: 2 s 373 ms, fetching: 14 ms)
```
