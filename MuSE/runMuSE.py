#!/usr/bin/python
import sys
import os
from subprocess import call
import re
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run MuSE on list of paired files')
	parser.add_argument('-f', '--files', help="Txt file containing list of file locations", nargs=1, required=True, type=str)
	args = parser.parse_args()

	with open(args.files[0], 'r+') as files:
		for x in files:
			line = x.split("\t")
			Tumor = line[0]
			Normal = line[1]
			prefix = line[2].rstrip('\n')
			with open(prefix+ "_MuSE.lsf", 'w+') as lsf:
				lsf.write("#BSUB -J " + prefix + '\n')
				lsf.write("#BSUB -W 24:00" + '\n')
				lsf.write("#BSUB -o /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
				lsf.write("#BSUB -e /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
				lsf.write("#BSUB -cwd /rsrch2/PanCanRsch/jhuang14/MolBarcode" + '\n')
				lsf.write("#BSUB -q medium" + '\n')
				lsf.write("#BSUB -u jhuang14@mdanderson.org" + '\n')
				lsf.write("#BSUB -n 3" + '\n')
				lsf.write("#BSUB -M 32000" + '\n')
				lsf.write("#BSUB -R rusage[mem=32000]" + '\n')
				lsf.write("#BSUB -N" + '\n')
				lsf.write("#BSUB -B" + '\n')
				lsf.write("./MuSE.sh -t " + Tumor  + " -n " + Normal + " -o " + prefix)
			call("bsub < " + prefix + "_MuSE.lsf", shell = True)
