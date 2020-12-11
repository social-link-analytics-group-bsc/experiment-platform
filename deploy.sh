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

LOG_DIR="${PROJECT_DIR}/log"

if [[ ! -d $LOG_DIR ]]
then
    `mkdir $LOG_DIR`
fi

LOGFILE=${LOG_DIR}/deploy_expplat.log
ERRORFILE=${LOG_DIR}/deploy_expplat.err
error=0

#0. get into the app directory
echo "[1/6] Getting into the directory ${PROJECT_DIR}"
cd $PROJECT_DIR

#1. create backup
if [ $? -eq 0 ]
then
    echo "[2/6] Creating a backup in ${BACKUP_DIR}..."
    backup_dt=`date '+%Y-%m-%dT%H%M'`
    backup_fn="data${backup_dt}.json"
    docker-compose -f docker-compose.yml exec app python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ${BACKUP_DIR}/${backup_fn} >> $LOGFILE 2>> $ERRORFILE
else
    error=0
fi

#2. pull changes from master
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[3/6] Pulling changes from master..."
    git pull origin master
else
    error=0
fi

#3. down containers
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[4/6] Downing containers..."
    docker-compose -f docker-compose.yml down
else
    error=0
fi

#4. change permission of mysql directory
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[5/6] Change permission of mysql directory"
    sudo chmod 777 -R ${PROJECT_DIR}/mysql
else
    error=0
fi

#5. up containers
if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "[6/6] Building and running containers..."
    docker-compose -f docker-compose.yml up --build -d
else
    error=0
fi

if [[ $? -eq 0 ]] && [[ $error -eq 0 ]]
then
    echo "Process has finished successfully"
    echo "For more information, check $LOGFILE"
else
    echo "There was an error running the process"
    echo "For more information, check $ERRORFILE"
fi

exit $error