#!/bin/bash

# MODIFY BELOW - CHANGE THE BASE JOB NAME AND INPUT YEARS TO SUBMIT
# JOB NAME WILL BE "JOBBASE_YYYY", e.g. "pyjob_2021"
# UTILDIR="/uufs/chpc.utah.edu/common/home/lin-group19/ltk/bashutil"
BASEDIR="/uufs/chpc.utah.edu/common/home/lin-group19/ltk/GCOM-C"
LOG_BASEDIR="${BASEDIR}/log/CV-MVC"
JOBBASE="GCOM_CV-MVC"

QC_FLAG="basic"


YEARS=$(seq 2018 2019) # specify years to submit jobs for (will be used in the job script to determine which files to process)
COMPOSITES=$(seq 0 22)

GCOM_TILES=(
# "h09v04" # US-NR1
# "h10v06" # OSBS
# "h11v03" # Ca-Obs
# "h11v02" # DEJU
"h12v04" # US-UMB
# "h10v04" # US-Ne3
)


njobs=0

for GCOM_TILE in "${GCOM_TILES[@]}"; do
    LOGDIR="${LOG_BASEDIR}/${GCOM_TILE}"
    mkdir -p ${LOGDIR}/archive/ # create log dir and an archive dir to put old files

    for YYYY in ${YEARS}; do
        for COMPOSITE in ${COMPOSITES}; do

            echo "Submitting CV-MVC with ${QC_FLAG} QC flag - ${GCOM_TILE}, year ${YYYY}, composite period ${COMPOSITE}"
            COMPOSITE_2D=$(printf "%02d" ${COMPOSITE})
            # Define the job name
            JOBNAME="${JOBBASE}_${QC_FLAG}_${GCOM_TILE}_${YYYY}_${COMPOSITE_2D}"

            LOGDIR="${LOG_BASEDIR}/${GCOM_TILE}/${COMPOSITE_2D}_${QC_FLAG}"
            mkdir -p ${LOGDIR}/archive/ # create log dir and an archive dir to put old files

            # archive past log files tagged with this JOBBASE
            
            CUR_JOBBASE_FILES=$(find ${LOGDIR} -maxdepth 1 -type f -name "*${JOBNAME}*") # list existing log files tagged with this JOBBASE
            if [ ! -z "${CUR_JOBBASE_FILES}" ] # if there are any existing...
            then
                mv ${LOGDIR}/*${JOBNAME}* ${LOGDIR}/archive/ # move to the 'archive' dir
            fi

            # find other files older than 2 weeks
            OLD_FILES=$(find ${LOGDIR} -maxdepth 1 -type f -mtime +14) 
            if [ ! -z "${OLD_FILES}" ] # there are any old files....
            then
                for OLD_FILE in ${OLD_FILES}
                do
                mv ${OLD_FILE} ${LOGDIR}/archive/ # move old file to the 'archive' dir
                done
            fi

            # find old status report files and delete them
            rm -f ${LOGDIR}/RUN_STATUS*.txt

            # submit job to CHPC for this polygon
            sbatch -D $LOGDIR --job-name=$JOBNAME --export=LOGDIR=${LOGDIR},GCOM_TILE=${GCOM_TILE},YYYY=${YYYY},COMPOSITE=${COMPOSITE},QC_FLAG=${QC_FLAG},JOBNAME=${JOBNAME} $BASEDIR/code/02~pyjob.sbatch
            njobs=$((njobs+1))
        done
    done
done

echo "Submitted ${njobs} sbatch jobs"
