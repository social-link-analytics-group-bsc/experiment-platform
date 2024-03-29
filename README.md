# Experiment Platform

## Installation and Execution

1. Install docker and docker-compose in your local machine. Check out the official installation [guidelines](https://docs.docker.com/install);
2. Clone the repository `git clone https://github.com/social-link-analytics-group-bsc/experiment-platform.git`;
3. Get into the directory `experiment-platform/experiment`;
4. Change current branch to *container-dev*, `git checkout contrainer-dev`;
5. Run `scripts/prepare-config-templates.sh`
6. Set the configuration parameters of the database in `.env`;
7. Set the `SECRET_KEY` as well as the configuration parameters of the database in `.env`;
8. Build docker container `docker-compose -f docker-compose.yml up --build -d`. Once containers are fully created, you can watch the logs with `docker-compose -f docker-compose.yml logs -f`, to see for the containers to be fully initialized;
9. Load initial data `docker-compose -f docker-compose.yml exec app python manage.py loaddata expplat`;
10. Go to `http://localhost:1550/expplat` to access the tool