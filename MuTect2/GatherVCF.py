#!/usr/bin/python
import sys
import os
from subprocess import call
import re
import argparse

## read in path
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run mutect on list of files')
	parser.add_argument('-f', '--path', help="Path to folder containing vcfs of files", nargs=1, required=True, type=str)
	args = parser.parse_args()

	if args.path[0] != "/":
		path = args.path[0] + "/"
	else:
		path = args.path[0]
## sample name
	sample = os.path.basename(os.path.normpath(path))

## Need to input files in genomic order i.e 1:22
## issue is that files are alphanumeric so order goes 10:19, 1, 2, 20:22, 3:9
## However it is also necessary to check to see if the files do exist first before doing anything more.
## Two ways of looking at this problem.
## A: Write a file containing 1:22 while seeing if the file exists. If doesn't exit with error
## B: search folder first before making list.
## A is easier probably
	with open(sample + "_GatherVCF.lsf", "w+") as lsf:
		lsf.write("#BSUB -J " + sample + "_GatherVCF" + '\n')
		lsf.write("#BSUB -W 1:00" + '\n')
		lsf.write("#BSUB -o /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
		lsf.write("#BSUB -e /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
		lsf.write("#BSUB -cwd /rsrch2/PanCanRsch/jhuang14/MolBarcode" + '\n')
		lsf.write("#BSUB -q short" + '\n')
		lsf.write("#BSUB -u jhuang14@mdanderson.org" + '\n')
		lsf.write("#BSUB -n 1" + '\n')
		lsf.write("#BSUB -M 12000" + '\n')
		lsf.write("#BSUB -R rusage[mem=12000]" + '\n')
		lsf.write("#BSUB -N" + '\n')
		lsf.write("#BSUB -B" + '\n')
		lsf.write("module load gatk/4.1.0.0" + '\n')
		lsf.write("gatk GatherVcfs -O " + path + sample + ".umi.filtered.combined.vcf.gz")
		for x in range(1,23):
			vfile = path + sample + ".umi.sorted_chr" + str(x) + ".filtered.vcf.gz"
			lsf.write(" \\\n")
			try:
				f = open(vfile, 'r')
				lsf.write("\t-I " + vfile)
			except FileNotFoundError:
				print("Missing " + vfile)
				print("Exiting")
				sys.exit(1)
	call("bsub < " + sample + "_GatherVCF.lsf", shell = True)
