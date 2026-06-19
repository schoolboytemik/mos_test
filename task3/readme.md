# ETL Pipeline: CSV / JSON / XML / XLSX → PostgreSQL Data Vault

## Описание проекта

Проект реализует end-to-end ETL-пайплайн для загрузки данных из различных источников в PostgreSQL с последующим построением хранилища данных по модели Data Vault и выполнением аналитических SQL-запросов.

Входные данные имели следующие форматы:

* CSV
* JSON
* XML
* XLSX

Используемый стек:

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Apache Airflow
* Docker

---

# Архитектура решения

```text
Исходные данные
(CSV / JSON / XML / XLSX)
            │
            ▼
      normalize.py
            │
            ▼
     data/cleaned/*.csv
            │
            ▼
       load_raw.py
            │
            ▼
        RAW Layer
            │
            ▼
       load_sor.py
            │
            ▼
      Data Vault (SOR)
            │
            ▼
      SQL-аналитика
```

---

# Структура проекта

```text
task3/
│
├── dags/
│   └── etl_pipeline.py
│
├── data/ 
│   ├── customers.csv
│   ├── orders.json
│   ├── payments.csv
│   ├── products.xlsx
│   ├── events.xml
│   │
│   └── cleaned/
│       ├── customers.csv
│       ├── orders.csv
│       ├── payments.csv
│       ├── products.csv
│       ├── events.csv
│       └── problems.txt
│
├── ddl/
│   ├── 01_raw.sql
│   └── 02_sor.sql
│
├── sql/
│   ├── customers_without_orders.sql
│   ├── last_activity_of_top_5.sql
│   ├── most_popular_goods.sql
│   ├── revenue_by_month.sql
│   └── top_10_customers.sql
│
├── src/
│   ├── transform/
│   │   └── normalize.py
│   │
│   ├── load_raw.py
│   └── load_sor.py
│
├── .gitignore
├── docker-compose.yml
├── readme.md
├── requirements.txt
└── общение с ИИ.md
```

---

# Слои хранения данных

## RAW

Слой предназначен для хранения очищенных и нормализованных данных, максимально близких к исходным источникам.

Таблицы:

* raw.customers
* raw.products
* raw.orders
* raw.payments
* raw.events

Дополнительно в таблицах RAW сохраняются технические поля:

- load_dttm — дата и время загрузки записи;
- source_file — имя файла-источника, из которого была загружена запись.

---

## Data Vault (SOR)

Реализована модель Data Vault, включающая:

### Hubs:

* hub_customer
* hub_product
* hub_order
* hub_payment
* hub_event

### Satellites:

* sat_customer
* sat_product
* sat_order
* sat_payment
* sat_event

### Links:

* link_customer_order
* link_order_product
* link_order_payment
* link_customer_event
* link_event_product

Для формирования Hub Keys и HashDiff используются MD5-хэши.

---

# Инкрементальная загрузка

Для предотвращения появления дубликатов используются ограничения UNIQUE:

- на бизнес-ключи Hub-таблиц;
- на пары (hub_key, hashdiff) в Satellite-таблицах;
- на пары связанных ключей в Link-таблицах.

При загрузке данных используется конструкция:

```sql
ON CONFLICT DO NOTHING
```

Это позволяет выполнять повторные запуски того же набора данных без появления дублирующихся записей, что однако **не обеспечивает** полноценную промышленную инкрементальность.

---

# Принятые решения по Data Quality

## Общий подход

Для упрощения дальнейшей загрузки в БД все входные данные приводятся к единому формату CSV.

При обнаружении некорректных значений записи не удаляются, а проблемные поля приводятся к пустым значениям (`NULL`), а информация о проблеме сохраняется в лог-файл:

```text
data/cleaned/problems.txt
```

Такой подход позволяет сохранить максимальный объем данных и избежать потери потенциально полезной информации.

После извлечения данные проходят этап нормализации и очистки, результат сохраняется в промежуточном слое:

```text
data/cleaned
```

который используется для последующей загрузки в PostgreSQL.

---

# Автоматизация

Оркестрация ETL реализована в Apache Airflow.

DAG состоит из трех последовательных этапов:

```text
normalize
    ↓
load_raw
    ↓
load_sor
```

### normalize

Чтение исходных файлов, очистка и нормализация данных.

### load_raw

Загрузка очищенных данных в слой RAW.

### load_sor

Заполнение Data Vault (Hub, Satellite, Link).

---

# Аналитические запросы

Реализованы следующие SQL-запросы:

* Топ-10 клиентов по сумме покупок
* Выручка по месяцам
* Самые популярные товары
* Последняя активность топ-5 клиентов по количеству покупок
* Пользователи без заказов

Все запросы находятся в каталоге:

```text
sql/
```

---

# Запуск проекта

## Требования

* Docker
* Docker Compose
* WSL (для Windows) либо Linux

Python и локальное виртуальное окружение требуются только для разработки и отладки. Для запуска проекта достаточно Docker.

## Шаг 1. Запуск контейнеров

```bash
docker compose up -d
```

После запуска будут автоматически созданы:

* база данных PostgreSQL;
* схемы RAW и SOR;
* сервисы Apache Airflow.

## Шаг 2. Открыть Airflow

Перейти по адресу:

```text
http://localhost:8080
```

Учетные данные:

```text
login: admin
password: admin
```

## Шаг 3. Запустить ETL

В интерфейсе Airflow запустить DAG:

```text
etl_pipeline
```

После успешного выполнения данные будут загружены в PostgreSQL и преобразованы в модель Data Vault.

---

# Воспроизведение результатов

После выполнения DAG можно подключиться к PostgreSQL, используя терминал:

```bash
docker exec -it postgres psql -U postgres -d mos
```

Проверить загрузку данных:

```sql
SELECT COUNT(*) FROM raw.customers;
SELECT COUNT(*) FROM raw.orders;

SELECT COUNT(*) FROM sor.hub_customer;
SELECT COUNT(*) FROM sor.sat_customer;
SELECT COUNT(*) FROM sor.link_customer_order;
```

Для выполнения аналитических запросов:

```sql
\i /sql/top_customers.sql
\i /sql/revenue_by_month.sql
\i /sql/popular_products.sql
```
