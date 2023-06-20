# fastAPI_tutorial

cd fastAPI_tutorial

uvicorn app.main:app --reload

1. set variable environment
`export my_db_url="localhost:5432"`

2. init alembic
`alembic init alembic`

3. export requriement 
`pip list --format=freeze > requirements.txt`

git push heroku master:main

4. run docker
`docker-compose -f docker-compose-dev.yml up` -- show reloading information in cmd <br>
`docker-compose -f docker-compose-dev.yml up -d` -- dont show reloading information in cmd
5. deactivate conda virtual environment
`conda deactivate`
6. activate conda virtual environment in current directory
`conda activate ./venv`
7. run pytest
`pytest -v -s` 