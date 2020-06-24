# Blog built using Flask
* FrontEnd: HTML, CSS, Bootstrap
* Database: Postgresql (both local and deployment -- Heroku)

# How to run the application locally?
* Change parameters, information in info.json file.
* Setup postgresql client on your machine.
* Create local database and replace the name of db with your db name in <b> blog.py </b>:
```
database_url = os.getenv(
    'DATABASE_URL',
    default='postgresql://postgres:12345@localhost:5432/your-db-name',
)
```
* Run blog.py file.

# How to deploy the app on Heroku?
* Create new app on Heroku.
* Link the app to GitHub Repository.
* Manually Create Postgres instance.
* Push the changes to Heroku Remote.

# Blog Link 
https://flask-heroku-blog.herokuapp.com/