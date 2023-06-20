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
`docker-compose -f docker-compose-dev.yml up`