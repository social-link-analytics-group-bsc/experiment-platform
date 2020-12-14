#!/bin/bash

###
# Before running this pull 
# new changes the master branch
# of the repository by executing
# the command `git pull origin master`
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

LOG_DIR="${PROJECT_DIR}/log"

if [[ ! -d $LOG_DIR ]]
then
    `mkdir $LOG_DIR`
fi

ERRORFILE=${LOG_DIR}/deploy_expplat.err
error=0

#0. get into the app directory
echo "[1/5] Getting into the directory ${PROJECT_DIR}"
cd $PROJECT_DIR

#1. create backup
if [ $? -eq 0 ]
then
    echo "[2/5] Creating a backup in ${BACKUP_DIR}..."
    backup_dt=`date '+%Y-%m-%dT%H%M'`
    backup_fn="data${backup_dt}.json"
    docker-compose -f docker-compose.yml exec app python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ${BACKUP_DIR}/${backup_fn} 2>> $ERRORFILE
else
    error=1
fi

#2. down containers
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[3/5] Downing containers..."
    docker-compose -f docker-compose.yml down
else
    error=1
fi

#3. change permission of mysql directory
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[4/5] Change permission of mysql directory"
    sudo chmod 777 -R ${PROJECT_DIR}/mysql
else
    error=1
fi

#4. up containers
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[5/5] Building and running containers..."
    docker-compose -f docker-compose.yml up --build -d
else
    error=1
fi

if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "Process has finished successfully"
else
    echo "There was an error running the process"
    echo "For more information, check $ERRORFILE"
fi

exit $error