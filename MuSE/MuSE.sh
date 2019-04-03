#!/bin/bash

usage() {
    echo "Usage: $0 [-t <string>] [-n <string>] [-o <string>]"
    echo "    -t tumor bam"
    echo "	  -n normal bam"
    echo "	  -o output prefix"
    exit 1;
}
while getopts ":t:n:o:" x; do
    case "${x}" in
        t)
            t=${OPTARG}
            ;;
        n)
            n=${OPTARG}
            ;;
        o)
            o=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
if [ -z ${t} ]; then
    usage
fi
if [ -z ${n} ]; then
    usage
fi



## MuSE call –O Output.Prefix –f Reference.Genome Tumor.bam Matched.Normal.bam
## MuSE sump -I Output.Prefix.MuSE.txt -G –O Output.Prefix.vcf –D dbsnp.vcf.gz


MuSE call -O $o -f ~/MolBarcode/ref/hg19_k/hg19.fasta $t $n
MuSE sump -I ${o}.MuSE.txt -E -O ${o}.vcf -D common_all.vcf.gz
