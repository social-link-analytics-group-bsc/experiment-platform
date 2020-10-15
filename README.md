# experiment-platform

## Quickstart guide

#### Database configuration

Make sure you have MySQL instance running and a specific schema for the project. Apply the schema and credentials configuration in
```/experiment/settings.py``` at ```DATABASES``` variable.

#### Migrate the database

Run the following commands to create the database structure:

```
python manage.py makemigrations expplat
```

```
python manage.py migrate
```

Create the super admin user that will access the database:
```
python manage.py createsuperuser
```

#### Load initial data

Run the following command to load the initial data so that the platform can work:

````
python manage.py loaddata expplat
````

#### Visit the platform

Activate the platform:

````
python manage.py runserver
````

Finally everything is prepared. Add to the url given in the terminal ````/expplat```` and follow the steps.