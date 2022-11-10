# GORNIAC_SHOP
Web store "GORNIAC" of custom vape liquid (WARNING: This is ONLY student project) &lt;3
## Using:
Frontend:
- html, css, js  

Backend: 
- Python 3.10, FastAPI, Pydantic, jinja2Templates, SQLAlchemy, postgreSQL, Pillow

Docker

## Starting:
1. Change config in `cfg.py`
### With docker:
2. Insert files for logo (if you need it) to `/logo_docker`
3. Run `docker-script.bat` to create docker network and start docker-compose
### Without docker:
2. Insert files for logo (if you need it) to `core/static/logo`
3. Install requirements `$pip install -r requirements.txt` 
4. Start your postgres database
5. Create database by sql script `init database/create_database.sql` 
6. Start `server.py` 

## Manage store:
You can manage store by admin panel.
You should login by admin first and the go to `localhost:8000/admin_panel` 

## Example:
You can use example proudcts, if added it to database by `postgresql/example_database.sql` 
