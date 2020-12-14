#!/bin/bash

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

ERRORFILE=${LOG_DIR}/backup_expplat.err
error=0

#0. get into the app directory
echo "[1/2] Getting into the directory ${PROJECT_DIR}"
cd $PROJECT_DIR

#1. create backup
if [ $? -eq 0 ]
then
    echo "[2/2] Creating a backup in ${BACKUP_DIR}..."
    backup_dt=`date '+%Y-%m-%dT%H%M'`
    backup_fn="data${backup_dt}.json"
    docker-compose -f docker-compose.yml exec app python manage.py dumpdata --exclude auth.permission --exclude contenttypes > ${BACKUP_DIR}/${backup_fn} 2>> $ERRORFILE
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