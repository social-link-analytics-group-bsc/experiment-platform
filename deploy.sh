#!/bin/bash

###
# Before running this script change 
# the permission of the directory
# mysql by executing
# sudo chmod 777 -R mysql
###

PROJECT_DIR=`pwd`
BACKUP_DIR=`pwd`

for arg in "$@"
do
    case $arg in
        --project_dir=*)
        PROJECT_DIR="${arg#*=}"
        shift # Remove --project_dir= from processing
        ;;
        --backup_dir=*)
        BACKUP_DIR="${arg#*=}"
        shift # Remove --user_collection= from processing
        ;;
    esac
done

#0. get into the app directory
echo "Getting into the directory ${PROJECT_DIR}..."
cd $PROJECT_DIR

#1. create backup
echo "Creating a backup in ${BACKUP_DIR}..."
backup_dt=`date '+%Y-%m-%dT%H%M'`
backup_fn="data${backup_dt}.json"
docker-compose -f docker-compose.yml exec app python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ${BACKUP_DIR}/${backup_fn}

#2. pull changes from master
git pull origin master

#3. down containers
docker-compose -f docker-compose.yml down

#4. up containers
docker-compose -f docker-compose.yml up --build -d