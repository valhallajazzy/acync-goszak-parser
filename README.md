# Асинхронный парсер сайта  https://zakupki.gov.ru

Данный парсер собирает информацию по закупкам 44-ФЗ с перых двух страниц и выводит ее в консоль
Так же статус выполнения задачи можно отследить во Flower

## Подготовка и запуск скрипта
Все перечисленные пункты ниже деалются из корневой директории проекта в терминале

* Устанавливаем зависимости
```console
$ poetry install
```
* Активируем виртуальное окружение:
```console
$ poetry shell
```
* Если redis не установле на компьютере, можно его подтянуть в докере командой
```console
$ docker-compose up -d
```
* Создаем файл `.env` и указываем переменные `CELERY_BROKER_URL` и `CELERY_RESULT_BACKEND`
![Screenshot](https://github.com/valhallajazzy/online_library/blob/main/pic/pathtulu.png)
* В первом теримнале запускаем Celery:
```console
$ celery -A tasks.celery worker --loglevel=info
```
* Во втором теримнале запускаеме Flower:
```console
$  celery -A tasks:celery flower port=5555
```
* В третьем терминале запускаем наши задачи:
```console
$  python3 main.py
```
