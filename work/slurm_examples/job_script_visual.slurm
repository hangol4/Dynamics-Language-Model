#!/bin/bash
#SBATCH --job-name=PANORAMIC_project
#SBATCH --ntasks=1                     # tasks
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00           # time (HH:MM:SS)
#SBATCH -o slurm_output/JWST_%A_%a.out        # STDOUT
#SBATCH -e slurm_output/JWST_%A_%a.err        # STDERR
#SBATCH --mem=20G        # memory required
#SBATCH --mail-type=FAIL,END      # notifications for job done & fail
#SBATCH --mail-user=h.golawska@sms.ed.ac.uk  # send-to address

# python3 /home/hgolawska/summer_project/sed_plotter.py
python3 /home/hgolawska/summer_project/test_csv.py
