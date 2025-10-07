# TKP Generator

Сервис для формирования технико-коммерческих предложений (ТКП) с использованием FastAPI и OpenAI Structured Outputs.

## Возможности
- Интерактивный сбор недостающих данных через `/tkp/collect`.
- Рендеринг готового ТКП в формате Markdown через `/tkp/render`.
- Проверка состояния сервиса по `/healthz`.

## Быстрый старт
1. Скопируйте файл окружения и заполните ключ:
   ```bash
   cp .env.example .env
   ```
2. Укажите значения `OPENAI_API_KEY` и при необходимости модель в `.env`.
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Проверьте здоровье сервиса:
   ```bash
   curl http://localhost:8000/healthz
   ```

## Тестирование
```bash
pytest
```

## Структура проекта
```
.
├── app/
│   ├── main.py
│   ├── models.py
│   ├── openai_client.py
│   ├── settings.py
│   ├── services/
│   │   ├── tkp_schema.json
│   │   ├── tkp_renderer.py
│   │   └── totals.py
│   └── templates/
│       └── tkp.md.j2
├── tests/
│   └── test_totals.py
├── requirements.txt
├── Dockerfile
├── devcontainer.json
├── .vscode/launch.json
├── .env.example
├── .gitignore
└── README.md
```

## Docker
```bash
docker build -t tkp-generator .
docker run --rm -p 8000:8000 --env-file .env tkp-generator
```
