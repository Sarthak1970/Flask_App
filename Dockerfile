FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]