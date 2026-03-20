# EA1RKV - Radioclub Vigo-Val Miñor

Website for **EA1RKV** (Unión de Radioaficionados de Vigo-Val Miñor), built with [Wagtail CMS](https://wagtail.org/).

## Tech Stack

- **Wagtail 6.x** (Django-based CMS)
- **PostgreSQL 16** (database)
- **Gunicorn** (WSGI server for production)
- **Nginx** (reverse proxy for production)
- **Redis** (caching for production)
- **Docker Compose** (containerized deployment)
- **wagtail-localize** (trilingual content: ES/EN/GL)

## Features

- **Home page** with hero section, club info (callsign, frequency, locator), and latest blog posts
- **Blog** with Draftail rich text editor, featured images, tags, and pagination
- **Trilingual support** (Español, English, Galego) via wagtail-localize
- **Search** functionality
- **Responsive design** with mobile-first approach
- **Wagtail admin** for content management with group permissions

## Quick Start (Docker)

```bash
# Clone the repository
git clone <repository-url>
cd wagtail_example

# Start the development environment
docker compose up --build

# In another terminal, create a superuser
docker compose exec web python manage.py createsuperuser
```

The site will be available at **http://localhost:8000** and the admin at **http://localhost:8000/admin/**.

## GitHub Codespaces

This project includes a `.devcontainer` configuration for GitHub Codespaces:

1. Click **"Code" > "Codespaces" > "Create codespace on main"**
2. Wait for the environment to build
3. The site starts automatically at port 8000
4. Default admin credentials: `admin` / `admin`

## Local Development (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

> **Note:** Without Docker, the project uses SQLite by default.

## Initial Content Setup

After starting the site and logging into the admin:

1. Go to **Settings > Sites** and ensure a site is configured for `localhost:8000`
2. The **Home Page** is created automatically. Edit it to add:
   - Hero title and subtitle
   - Club callsign, frequency, and locator
   - Club description
3. Create a **Blog Index Page** as a child of the Home Page:
   - Go to **Pages > Home > Add child page > Blog Index**
4. Create **Blog Posts** as children of the Blog Index:
   - Go to the Blog Index page > **Add child page > Blog Post**
   - Use the Draftail editor for rich content
   - Add featured images and tags

## User Permissions

Wagtail has a built-in group permissions system. To set up editor access:

1. Go to **Settings > Groups** in the Wagtail admin
2. Create an **Editors** group:
   - Add permissions: "Add" and "Edit" on Blog pages
   - Add "Choose" permission on Images and Documents
3. Create a **Moderators** group:
   - Add all Editor permissions plus "Publish"
4. Create user accounts and assign them to the appropriate group

Operators can then log into `/admin/` and create/edit blog posts using the Draftail editor.

## Production Deployment

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your production values

# Start production environment
docker compose -f docker-compose.prod.yml up --build -d

# Create superuser
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

The production setup includes:
- Gunicorn as the WSGI server
- Nginx as reverse proxy (serves static/media files)
- Redis for caching
- PostgreSQL with persistent storage

## Project Structure

```
wagtail_example/
├── ea1rkv/              # Django project package
│   ├── settings/        # Split settings (base/dev/production)
│   ├── static/          # Project-level static files (CSS/JS)
│   ├── urls.py          # URL configuration with i18n
│   └── wsgi.py
├── home/                # Home page app
│   ├── models.py        # HomePage model
│   └── templates/
├── blog/                # Blog app
│   ├── models.py        # BlogIndexPage, BlogPage, BlogPageTag
│   └── templates/
├── search/              # Search functionality
├── templates/           # Global templates (base.html, header, footer)
├── docker/              # Docker config (nginx, entrypoint)
├── .devcontainer/       # GitHub Codespaces config
├── Dockerfile
├── docker-compose.yml       # Development
├── docker-compose.prod.yml  # Production
└── requirements.txt
```

## Navigation

The site includes navigation with placeholders for future features:

| Menu Item    | Status        |
|-------------|---------------|
| Inicio      | Active        |
| Blog        | Active        |
| El Club     | Coming soon   |
| Actividades | Coming soon   |
| Galería     | Coming soon   |
| Diplomas    | Coming soon   |
| Manuales    | Coming soon   |
| Repetidores | Coming soon   |
| Contacto    | Coming soon   |

## License

This project is for the EA1RKV radio club. All rights reserved.
