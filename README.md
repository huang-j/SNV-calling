# SNV-calling
Runs on Mutect2/MuSE with some processing for SureCall

Each caller has it's own annotationfilter file because of different structuring.

SureCall
========

agiprocv2.sh // Requires Agent from Agilent, bwa-mem, samtools
  Inputs: 
    -d bottom directory
    -l a list of samples to be processed
    -b bed file
  Outputs:
    Trimmed/: trimmed fastq
    Bams/: Barcode collapsed and unbarcode collapsed samples
   
SureCallAnnotationFilter.R
  Inputs:
    Annovar annotated vcf file off of SureCall (SNPPT)
  Outputs:
    filtered table

MuSE
====

rMuSE.sh // Requires MuSE, pretty much no other documentation other than those two lines
  Has to be paired samples
  in form:
  path/to/tumor path/to/normal  samplename
  
runMuSE.py // For HPC jobs

MuTect2
=======

rMutect2Chr.sh // Requires gatk/4.1.0.0+ (4.0 has weird issues with Mutect) 
  Runs Mutect. Note the usage() for required fields
  
runMutect2Chr.py // unpaired
runMutect2MatchChr.py // paired
  Both generate Jobs for the HPC. To run chr by chr it's necessary to input a interval file of just that chr.
  e.g. in bash:
  for f in $(find {location of interval files} | grep 'chr') ; do
    python runMutect2MatchChr.py -f [tab separated paired file locations] -i $f
  done

GatherVCF.py //also requires gatk/4.1.0.0+
  combines the VCF files from chr to chr runs to one single VCF
  note: only does chr1:22 (no M, X, Y)
  
gatkPoN.sh
  create PoN from single sample Mutect2 runs
