#!/usr/bin/python
import sys
import os
from subprocess import call
import re
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run mutect on list of files')
	parser.add_argument('-f', '--files', help="Txt file containing list of file locations, tab separated", nargs=1, required=True, type=str)
	parser.add_argument('-i', '--interval', help="Interval list", nargs=1, required=True, type=str)
	args = parser.parse_args()

	with open(args.files[0], 'r+') as files:
		for x in files:
			s = x.split("\t")
			dn = os.path.dirname(s[0])
			sampname = s[0].split("/")[-1].split('.')[0]
			normname = s[1].split("/")[-1].split('.')[0]
			if "chr" in args.interval[0]:
				chr = args.interval[0].split("/")[-1].split(".")[1]
			else:
				chr = ""
			with open(sampname + chr + "_Paired.lsf", 'w+') as lsf:
				lsf.write("#BSUB -J " + sampname + chr + '_Paired\n')
				lsf.write("#BSUB -W 24:00" + '\n')
				lsf.write("#BSUB -o /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
				lsf.write("#BSUB -e /rsrch2/PanCanRsch/jhuang14/logs" + '\n')
				lsf.write("#BSUB -cwd /rsrch2/PanCanRsch/jhuang14/MolBarcode" + '\n')
				lsf.write("#BSUB -q medium" + '\n')
				lsf.write("#BSUB -u jhuang14@mdanderson.org" + '\n')
				lsf.write("#BSUB -n 6" + '\n')
				lsf.write("#BSUB -M 24000" + '\n')
				lsf.write("#BSUB -R rusage[mem=24000]" + '\n')
				lsf.write("#BSUB -N" + '\n')
				lsf.write("#BSUB -B" + '\n')
				lsf.write("./rMutect2MatchChr.sh -b " + s[0].rstrip('\n') + " -r ref/hg19_k/hg19.fasta" + " -t " + sampname + " -n " + s[1].strip('\n') + " -p " + normname + " -l " + args.interval[0] + " -c " + chr )
			call("bsub < " + sampname + chr +  "_Paired.lsf", shell = True)
