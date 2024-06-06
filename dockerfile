FROM python:3.11-slim

# Устанавливаем pipenv
RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

# Устанавливаем зависимости из Pipfile
RUN pipenv install --deploy --system

# Копируем остальные файлы в рабочую директорию
COPY . .

# Установка Google Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates dirmngr && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Запускаем ваше приложение (замените на вашу команду)
CMD ["python", "kwork.py"]