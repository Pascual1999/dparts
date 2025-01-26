
# Dparts

Servidor basado en Django para la administración y el soporte de las operaciones de la página web.


## Instalación

Desde la carpeta del proyecto:

```bash
  pip install pipenv --user
  pipenv install
```
    

## Montar servidor local

Ejecutar migraciones:
```bash
  pipenv python manage.py makemigrations
  pipenv python manage.py migrate
```
Montar el servidor:

```bash
  pipenv shell
  python manage.py runserver
```
## Variables de entorno

Para ejecutar este proyecto, se necesitará configurar las siguientes Variables de entorno.

`SECRET_KEY`

`DATABASE_URL`

`DEBUG`

`USE_SQLITE`

Compatible con los archivos .env


## Ejecutar Pruebas

Pruebas unitarias:

```bash
  pipenv shell
  python manage.py test --tag=unit_tests -v 2
```

Pruebas funcionales:


```bash
  pipenv shell
  python manage.py test --tag=functional_tests -v 2
```
