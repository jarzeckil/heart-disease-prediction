FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="${PYTHONPATH}:/app/src"

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root
COPY src ./src
COPY models ./models

CMD ["uvicorn", "src.heart_failure_prediction.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
