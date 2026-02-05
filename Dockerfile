# Базовый образ
FROM python:3.10

# Установка рабочей директории
WORKDIR /app

# Копирование всех файлов проекта в контейнер
COPY . /app/

# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Создание папки для сокетов
RUN mkdir -p /app/sockets

# Указание команды для запуска контейнера
CMD ["gunicorn", "--bind", "unix:/app/sockets/Granit.sock", "--access-logfile", "-", "--error-logfile", "-", "Granit.wsgi:application"]