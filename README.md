# URV EA1RKV - Radioclub Vigo Val Miñor

Web de la **Unión de Radioaficionados de Vigo - Val Miñor (EA1RKV)**, sección local de la [URE](https://www.ure.es/) (Unión de Radioaficionados Españoles).

Construida con [Wagtail CMS](https://wagtail.org/) 6.0 sobre Django.

## Estructura del Proyecto

```
radioclub_site/
├── core/           # Bloques StreamField, template tags, context processors
├── home/           # Página de inicio con hero y secciones destacadas
├── about/          # Nosotros, junta directiva, historia
├── blog/           # Noticias y artículos con categorías
├── activities/     # Concursos, diplomas y eventos
├── radio/          # Secciones técnicas (satélites, HF, VHF/UHF, APRS, meteo)
├── contact/        # Formulario de contacto con mapa
├── gallery/        # Galerías de fotos
└── search/         # Búsqueda en el sitio
```

## Desarrollo con GitHub Codespaces

1. Abre el repositorio en GitHub Codespaces
2. El entorno se configura automáticamente (instala dependencias, migra la BD y crea datos iniciales)
3. El servidor se inicia en el puerto 8000
4. Accede al admin en `/admin/` con usuario `admin` / contraseña `admin`

## Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
cd radioclub_site
python manage.py migrate

# Crear datos iniciales (superusuario admin/admin + estructura de páginas)
python manage.py seed_initial_data

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## Tests

```bash
cd radioclub_site
python manage.py test
```

## Producción con Docker

```bash
# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Iniciar servicios
docker compose up -d

# Crear superusuario en producción
docker compose exec web python manage.py createsuperuser
```

### Variables de entorno (producción)

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `ALLOWED_HOSTS` | Dominios permitidos (separados por comas) |
| `DATABASE_URL` | URL de conexión PostgreSQL |
| `CSRF_TRUSTED_ORIGINS` | Orígenes de confianza para CSRF |
| `SECURE_SSL_REDIRECT` | Redirigir a HTTPS (default: True) |
| `WAGTAILADMIN_BASE_URL` | URL base del sitio |

## Tecnologías

- **Backend:** Python 3.12, Django 6.0, Wagtail 6.0
- **Frontend:** Bootstrap 5.3, Bootstrap Icons
- **Base de datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Servidor:** Gunicorn + WhiteNoise
- **Contenedores:** Docker + Docker Compose
- **Desarrollo:** GitHub Codespaces / DevContainers
