FROM python:3.11-slim

# Устанавливаем pipenv
RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

# Устанавливаем зависимости из Pipfile
RUN pipenv install --deploy --system

# Копируем остальные файлы в рабочую директорию
COPY . .

# Запускаем ваше приложение (замените на вашу команду)
CMD ["python kwork.py"]