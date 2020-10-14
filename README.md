# experiment-platform

## Quickstart guide

#### Database configuration

Make sure you have MySQL instance running and a specific schema for the project. Apply the schema and credentials configuration in
```/experiment/settings.py``` at ```DATABASES``` variable.

#### Migrate the database

```
python manage.py makemigrations expplat
```

```
python manage.py migrate
```

```
python manage.py createsuperuser
```

#### Create experiment and install initial data

````
python manage.py runserver
````

Open you browser on the url provided in the terminal. You will see an error page, add ```/admin``` at the end of the url.

Enter the username and password of the superuser created previously. Once inside the admin dashboard, create a new experiment.

Now you can enter the web url adding ````/expplat/inst````. If the loading of initial data goes as expected, you will head to the index html.

#### Visit the platform

Finally everythin is prepared. Add to the url given in the terminal ````/expplat```` and follow the steps.