#!/bin/bash -l
#SBATCH -t 4:00:00
#SBATCH -J run_cosmosis
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --output=slurm_output/cosmosis_%A_%a.log
#SBATCH -e slurm_output/cosmosis_%A_%a.err
#SBATCH --mail-type=FAIL,END      # notifications for job done & fail
#SBATCH --mail-user=h.golawska@sms.ed.ac.uk  # send-to address

module purge
module load anaconda
source /usr/local/anaconda/3.11/etc/profile.d/conda.sh
conda activate /home/hgolawska/shproject/env
source cosmosis-configure
export OMP_NUM_THREADS=1

echo START $(date)
cd cosmosis-standard-library
mpirun -n 32 cosmosis --mpi examples/des-y3-shear_grid.ini
echo END $(date)
