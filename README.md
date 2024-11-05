
# DRF AirCraft Manager Project

Django Rest Framework ile Uçak Üretim Uygulaması.

Not: Projeyi docker üzerinden ayağa kaldırıyoruz, database olarak postgresql kullanıyoruz. 
Docker ile çalıştırmak istenmezse localde çalıştırırken db.sqlite3 kullanıyoruz.
Sonuç olarak postgresql'i docker üzerinden çalıştırırken kullanıyoruz docker'a bağlı değilken de db.sqlite3'ü kullanıyoruz.

# Kullanılan Teknolojiler
- Python
- Django
- Django Rest Framework
- Docker
- Postgresql
- Swagger
- HTML/CSS
- JAVASCRIPT


# Projeyi Docker Üzerinde Çalıştırma

Docker'ın olduğu dizinde şu komutla build alıyoruz ve proje çalışmaya başlıyor

```bash
docker-compose up --build
```

# Docker Kullanmadan Proje Çalıştırılmak İstenirse

Not: Sol taraftaki veriler Mac kurulumu için sağ taraftaki veriler Windows kurulumu içindir.

Projeyi Kurma  

```bash
 git clone 
```

Sanal Ortam Oluşturma
```bash
  python3 -m venv venv || python -m venv venv
```

Sanal Ortamı Aktif Etme
```bash
source venv/bin/activate  || venv\Scripts\activate
```

Gerekli Paketleri Kurma
```bash
  pip3 install -r requirements.txt  ||  pip install -r requirements.txt
```

Projeyi Çalıştımak için İlgili Dizine Gitme
```bash
  cd app/
```

Veri Tabanı Oluşturmak için Sırasıyla Yapılacaklar


```bash
  python3 manage.py makemigrations || python manage.py makemigrations
```

```bash
  python3 manage.py migrate || python manage.py migrate
```

Admin Paneline Giriş Yapacak User Oluşturma
```bash
  python3 manage.py createsuperuser || python manage.py createsuperuser
```

Not: admin paneline normalde username ve password ile giriş yapılırken, girişi özelleştirdiğim için email ve password bilgileri ile User oluşturup sisteme giriyoruz


Projeyi Çalıştırma
```bash
  python3 manage.py runserver || python manage.py runserver
```


# Swagger Kullanımı

Swagger ile projenin API dökümantasyonu oluşturulmuştur.

```http
  http://127.0.0.1:8000/api/docs/
```


# Login Sayfası

```http
  http://127.0.0.1:8000/login/
```


# Register Sayfası

```http
  http://127.0.0.1:8000/register/
```


# Dashboard Sayfası

```http
  http://127.0.0.1:8000/dashboard/
```


# Admin Paneli

Admin paneli olarak özelleştirilmiş django admin paketi olan jazzmin'i kullanıyoruz.

```http
  http://127.0.0.1:8000/admin/
```
