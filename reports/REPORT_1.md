## ДЗ №1 

1. [Базовая часть: Чекпоинты](#1-базовая-часть-чекпоинты)
2. [Нагрузочное тестирование](#2-нагрузочное-тестирование)
3. [Журнал проблем](#3-журнал-проблем)


## 1. Базовая часть: Чекпоинты

### 1.1. Проверка эндпоинтов (Health & Predict)

Проверка работоспособности API через `curl`:

**Health (GET /health):**
![Health Check](/screenshots/health_check_ok_1.png)

**Prediction (POST /v1/predict):**
![Post Check](/screenshots/post_check_ok_1.png)

---

### 1.2. Unit и API тесты (pytest)

Результат запуска тестов, покрывающих контракт (422 ошибки), smoke-тесты и детерминизм:

![Pytest Results](/screenshots/pytest_running_1.png)

---

### 1.3. Логи и запись в БД (SELECT)

Подтверждение того, что успешные предикты корректно записываются в таблицу `predictions` в PostgreSQL:

![Database Logs](/screenshots/log_to_postgre_1.png)

---

### 1.4. Docker Compose

Запуск сервиса через Docker Compose:

![Docker Compose](/screenshots/screenshot_docker_compose_up_good_1.png)

---

### 1.5. Kubernetes: Развертывание в Kind

Состояние подов в кластере Kind через `kubectl` и `k9s`, а также вызов `/predict` после `port-forward`

**Kubectl get pods:**
![Kubernetes Pods](/screenshots/screenshot_kube_1.png)

**K9s Interface:**
![K9s Pods](/screenshots/screenshot_kube_2_k9s.png)

---

## 2. Нагрузочное тестирование

Для оценки производительности сервиса было проведено нагрузочное тестирование с помощью **Locust** на 
`/v1/predict` и `/health`

### Результаты:

### Прогон 1: 10 пользователей, 5 req/s
![Load Test 10 users](/screenshots/screenshot_loading_test_1.png)

**Данные:**
- [run10_stats.csv](/run10_stats.csv) - итоговая статистика
- [run10_stats_history.csv](/run10_stats_history.csv) - история изменения во времени
- [run10_failures.csv](/run10_failures.csv) - упавшие запросы (пусто)
- [run10_exceptions.csv](/run10_exceptions.csv) - исключения (пусто)

### Прогон 2: 50 пользователей, 10 req/s
![Load Test 50 users](/screenshots/screenshot_loading_test_2.png)

**Данные:**
- [run50_stats.csv](/run50_stats.csv) - итоговая статистика
- [run50_stats_history.csv](/run50_stats_history.csv) - история изменения во времени
- [run50_failures.csv](/run50_failures.csv) - упавшие запросы (пусто)
- [run50_exceptions.csv](/run50_exceptions.csv) - исключения (пусто)

### Прогон 3: 100 пользователей, 20 req/s
![Load Test 100 users](/screenshots/screenshot_loading_test_3.png)

**Данные:**
- [run100_stats.csv](/run100_stats.csv) - итоговая статистика
- [run100_stats_history.csv](/run100_stats_history.csv) - история изменения во времени
- [run100_failures.csv](/run100_failures.csv) - упавшие запросы (пусто)
- [run100_exceptions.csv](/run100_exceptions.csv) - исключения (пусто)

### Выводы:

- На всех трех сценариях не появилось никаких ошибок.
- При увеличении нагрузки с 50 до 100 пользователей пропускная способность выросла с ~24.5 RPS до ~48.6 RPS - тоже почти в 2 раза. 
- Медиана (p50) была стабильной на всех 3-х тестах. Паталогического отклонения у p95 от неё не было, p95 заметно отклонилась от p50 начиная с 50 пользователей (14 мс при 10, 20мс при 50, 36мс при 100)


---

## 3. Журнал проблем



В процессе развертывания и тестирования возник ряд проблем, которые были успешно диагностированы и устранены.

### Проблема 1: Ошибка десериализации .joblib файла в сервисе

**Решение:** Ошибка была связан с тем, что модель обучал в отдельном ноутбуке, в котором версия sklearn была > 1.9. В проекте семинара работа велась в моделью, обученном с использованием scikit-learn 1.6.1. Добавил ноутбук в окружение проекта и обучил внутри него на этих же версиях библиотек.

### Проблема 2: Логи не записывались в БД

**Решение:** Проблема была связана с тем, что в add_task передавал статус ответа (`response.status_code`).  
`psycopg.errors.NotNullViolation: null value in column "status_code" of relation "predictions" violates not-null constraint`
Который не успевал сформироваться в момент вызова этого метода и фоновая задача падала при попытке записать null в колонку not null. Так как код должен доходить до этой строки при успешном выполнении метода, заменил на добавление 200, по умолчанию





