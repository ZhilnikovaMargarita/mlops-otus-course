
# Финальный проект по курсу MLOPS

**Структура проекта:**

- src/ - скрипты с подготовкой данных, инференсом и приложением
- model.pkl - модель
- requirements.txt - зависимости для запуска приложения c 
- Dockerfile.prod - сборка образа с приложением и моделью
- k8s/ - манифесты для запуска подов с приложением, prometheus, grafana

Kaggle:
https://www.kaggle.com/competitions/om-2022-ml-2-contest-2/overview

Docker Hub:
https://hub.docker.com/repository/docker/zhilnikova/mlops-otus-project/tags

P.S. За основу был взят репозиторий: https://github.com/sdukshis/otus-ml-skel/tree/main
