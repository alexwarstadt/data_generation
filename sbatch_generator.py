import argparse
import sys
import os
import random

def handle_arguments(cl_arguments):
    parser = argparse.ArgumentParser(description='')
    # Configuration files

    parser.add_argument('--number_runs', '-n', type=int,
                        help="Number of runs to generate")
    parser.add_argument('--slurm_dir', '-s', type=str,
                        help="Location where slurm scripts go")
    parser.add_argument('--data_dir', '-d', type=str,
                        help="Data directory ABOVE CoLA directory")
    parser.add_argument('--output_dir', '-o', type=str,
                        help="Location of output, where experiment name directory is created")
    parser.add_argument('--config_file', '-c', type=str, default="$JIANT_PROJECT_PREFIX/config/bert_tasks.conf",
                        help="location of config file")
    parser.add_argument('--exp_name', '-x', type=str,
                        help="Name of the experiment, i.e. directory name where all runs are contained")
    parser.add_argument('--max_epochs', '-e', type=str, default=10,
                        help="Maximum number of epochs")
    parser.add_argument('--lr', '-l', type=str, default="1E-5",
                        help="Learning rate")
    parser.add_argument('--val_interval', '-v', type=str, default="100",
                        help="How many batches between validation stages")
    parser.add_argument('--batch_size', '-b', type=str, default="32",
                        help="size of training batch")
    parser.add_argument('--grid_search', '-g', type=bool, default=False,
                        help="Whether to do grid search based on BERT hyperparameters")
    return parser.parse_args(cl_arguments)

header = """#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=7
#SBATCH --gres=gpu:p40:1
#SBATCH --mem=16GB
#SBATCH -t24:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

#PRINCE PRINCE_GPU_COMPUTE_MODE=default

# Run.\n"""


if __name__ == '__main__':
    args = handle_arguments(sys.argv[1:])
    experiment_dir = os.path.join(os.getcwd(), args.exp_name) if args.slurm_dir is None else args.slurm_dir
    if not os.path.isdir(experiment_dir):
        os.mkdir(experiment_dir)
    if args.grid_search:
        i = 0
        for lr in [0.00003, 0.00002, 0.00001]:
            for batch_size in [16]:
                for max_epochs in [4, 5, 10]:
                    slurm_file = os.path.join(experiment_dir, "run_%d.sbatch" % i)
                    out_file = open(slurm_file, "w")
                    out_file.write(header)
                    out_file.write("export JIANT_DATA_DIR=%s\n" % args.data_dir)
                    out_file.write("export NFS_PROJECT_PREFIX=%s\n" % args.output_dir)
                    out_file.write("python $JIANT_PROJECT_PREFIX/main.py --config_file " + args.config_file)
                    out_file.write(" --overrides \"run_name=run_" + str(i))
                    out_file.write(", max_epochs=" + str(max_epochs))
                    out_file.write(", lr=" + str(lr))
                    out_file.write(", val_interval=" + args.val_interval)
                    out_file.write(", exp_name=" + args.exp_name)
                    out_file.write(", random_seed=" + str(random.randint(1000, 10000)))
                    out_file.write(", batch_size=" + str(batch_size))
                    out_file.write("\"")
                    i += 1
    else:
        for i in range(int(args.number_runs)):
            slurm_file = os.path.join(experiment_dir, "run_%d.sbatch" % i)
            out_file = open(slurm_file, "w")
            out_file.write(header)
            out_file.write("export JIANT_DATA_DIR=%s\n" % args.data_dir )
            out_file.write("export NFS_PROJECT_PREFIX=%s\n" % args.output_dir)
            out_file.write("python $JIANT_PROJECT_PREFIX/main.py --config_file " + args.config_file)
            out_file.write(" --overrides \"run_name=run_" + str(i))
            out_file.write(", max_epochs=" + args.max_epochs)
            out_file.write(", lr=" + args.lr)
            out_file.write(", val_interval=" + args.val_interval)
            out_file.write(", exp_name=" + args.exp_name)
            out_file.write(", random_seed=" + str(random.randint(1000, 10000)))
            out_file.write(", batch_size=" + str(args.batch_size))
            out_file.write("\"")

