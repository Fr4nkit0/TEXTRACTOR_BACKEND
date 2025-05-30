# TEXTRACTOR_BACKEND

Un backend en Django REST Framework que permite el procesamiento de imágenes mediante OCR (Reconocimiento Óptico de Caracteres). Soporta motores como EasyOCR y PaddleOCR, incluye preprocesamiento de imágenes, manejo de idiomas y exportación de resultados a PDF.

## 🚀 Características principales
- 📷 Procesamiento de imágenes con EasyOCR y PaddleOCR
- 🧠 Preprocesamiento de imágenes para mejorar la precisión
- 🗣️ Soporte para múltiples idiomas
- 📄 Exportación a PDF o documento de texto

## Instalación local

### 1. Crear y activar entorno virtual

Se recomienda usar `venv` para crear un entorno virtual aislado.

```bash
# Crear entorno virtual llamado 'env'
python3 -m venv env

# Activar entorno virtual

# Linux
source env/bin/activate

```
### 2. Instalar dependencias

Una vez que tengas el entorno virtual activado, navega hasta la raíz del proyecto y ejecuta el siguiente comando para instalar todas las dependencias necesarias:

```bash
pip install -r requirements.base.txt
###2. Instalar dependencias
```

### 3. Configuración de credenciales

Dentro de la raíz del proyecto, crea un archivo llamado `.env` con la siguiente estructura:

```env
SECRET_KEY='django-insecure-$h$@!+v+v!!&87@v+ix22$%1d&r0x+7*nrd&rcm#t67a7t%81z'
DB_NAME='textractor_db'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='localhost'
DB_PORT='5432'
```
Nota: Asegúrate de modificar los valores de SECRET_KEY, DB_USER y DB_PASSWORD para que se ajusten a tu configuración local y mantén este archivo seguro, ya que contiene información sensible.
### 4. Configuración de la base de datos

Este proyecto utiliza **PostgreSQL** como sistema gestor de base de datos.  

Asegúrate de tener PostgreSQL instalado y en ejecución en tu máquina local antes de continuar.  

Si aún no lo tienes instalado, puedes descargarlo e instalarlo desde:  
[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Además, crea la base de datos con el nombre configurado en tu archivo `.env` (por defecto `textractor_db`) y verifica que el usuario y contraseña tengan los permisos necesarios para acceder a ella.

### 5. Crear y aplicar migraciones

Para crear las migraciones necesarias y aplicarlas a la base de datos, ejecuta los siguientes comandos:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
### 6. Ejecutar el proyecto

Para iniciar el servidor de desarrollo y levantar el backend, ejecuta:

```bash
python3 manage.py runserver
```


