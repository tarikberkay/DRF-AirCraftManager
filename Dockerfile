# Temel imaj olarak Python 3.12 kullanılıyor
FROM python:3.12-slim

# Çalışma dizini oluştur
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean

# Gereksinim dosyalarını kopyala
COPY requirements.txt /app/

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# FontAwesome 5'teki ugettext -> gettext değişikliğini yap
# RUN sed -i 's/ugettext/gettext/g' /usr/local/lib/python3.12/site-packages/fontawesome_5/fields.py

# Uygulama dosyalarını kopyala
COPY . /app/

WORKDIR /app/app/

# django.utils.translation içindeki ugettext çağrılarını gettext olarak değiştir
# RUN find /app -type f -name "*.py" -exec sed -i 's/ugettext/gettext/g' {} +

# Gerekli ortam değişkenlerini ayarla
ENV DJANGO_SETTINGS_MODULE=app.settings
ENV PYTHONUNBUFFERED=1

# migrate komutunu çalıştır
RUN python /app/app/manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]


# Port'u expose et
EXPOSE 8000