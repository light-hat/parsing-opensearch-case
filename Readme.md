# Кейс парсинга с Opensearch-аналитикой

Я решал задачу для себя, но может кому-то тоже пригодится.

Задача: Автоматически подбирать продукты в супермаркете под мой режим питания (подбор рациона для сушки) в заданном ценовом диапазоне.

Ближайшие задачи: доработка эмуляции поведения человека, реализация парсера как fastapi микросервиса, сохранение результатов работы в opensearch-индексы, CRUD по индексам.

```bash
sudo sysctl vm.max_map_count=262144
sudo apt update && sudo apt install -y git vim tmux
git clone https://github.com/light-hat/parsing-opensearch-case
cd parsing-opensearch-case
chmod +x provision.sh && sudo ./provision.sh
```
