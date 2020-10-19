# Experiment Platform

## Installation and Execution

1. Install docker and docker-compose in your local machine. Check out the official installation [guidelines](https://docs.docker.com/install);
2. Clone the repository `git clone https://github.com/social-link-analytics-group-bsc/experiment-platform.git`;
3. Get into the directory `experiment-platform/experiment`;
4. Change current branch to *container-dev*, `git checkout contrainer-dev`;
5. Run `scripts/prepare-config-templates.sh`
6. Set the configuration parameters of the database in `.env`;
7. Set the `SECRET_KEY` as well as the configuration parameters of the database in `.env`;
8. Build docker container `docker-compose -f docker-compose.dev.yml up --build -d`. Once containers are fully created, you can watch the logs with `docker-compose -f docker-compose.yml logs -f`, to see for the containers to be fully initialized;
9. Go to `http://localhost:8000/expplat` to access the tool

### Stop container

To stop containers run `docker-compose -f docker-compose.dev.yml down`

### Run container

To run containers without building them `docker-compose -f docker-compsoe.dev.yml up`. The option `-d` can be added to run containers in background.

### Clean-up

To start over from ground zero

1. Run `docker-compose -f docker-compose.prod.yml  down -v --rmi all --remove-orphans` to stop and remove containers
2. Execute `sudo rm -rf ./mysql` to remove `./mysql` volume
3. List docker images with `docker images`
4. Run `docker system prune` if you danglign images in your system