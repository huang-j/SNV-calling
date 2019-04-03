#!/bin/bash
## Runs Mutect2 and FilterMutectCalls

usage() {
    echo "Usage: $0 [-b <string>] [-r <string>] [-t <string>] [-l <string>] [-c <string>]"
    echo "        -b bam file"
    echo "        -r reference"
    echo "        -t tumor field"
    echo "        -l interval list for Mutect2"
    echo "        -c chr"
    exit 1;
}
while getopts ":b:r:t:l:c:" x; do
    case "${x}" in
        b)
            b=${OPTARG}
            ;;
        r)
            r=${OPTARG}
            ;;
        t)
            t=${OPTARG}
            ;;
        l)
            l=${OPTARG}
	    ;;
	c)
	    c=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${b}" ]; then
    usage
fi
if [ -z "${r}" ]; then
    usage
fi
if [ -z "${t}" ]; then
    usage
fi
if [ -z "${l}" ]; then
    usage
fi
if [ -c "${c}" ]; then
    usage
fi
echo "-b ${b}"
echo "-r ${r}"
echo "-t ${t}"
echo "-l ${l}"

echo "Calling Variants..."
gatk --java-options "-Xmx24G" Mutect2 -R ${r} \
-I ${b} \
-tumor ${t} \
--disable-read-filter MateOnSameContigOrNoMappedMateReadFilter \
--pon fonePoN.vcf.gz \
-L ${l} \
-O ${b%.bam}_${c}.vcf.gz

gatk --java-options "-Xmx24G" FilterMutectCalls \
-V ${b%.bam}_${c}.vcf.gz \
-O ${b%.bam}_${c}.filtered.vcf.gz \
--tumor-lod 3
