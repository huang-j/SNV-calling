#!/bin/bash
## this is primarily to have this available for remembering sake

usage() {
    echo "Usage: $0 [-l <string>] [-p <string>"
    echo "    -l file containing names of samples to be used. tab separated where second column is normals"
    echo "                e.g. MK29-T_S4"
    echo "	  -p output prefix"
    exit 1;
}
while getopts ":l:p:" x; do
    case "${x}" in
        l)
            l=${OPTARG}
            ;;
        p)
            p=${OPTARG}
            ;;

        *)
            usage
            ;;
    esac
done
if [ -z ${l} ]; then
    usage
fi
if [ -z ${p} ]; then
    usage
fi

gatk --java-options "-Xmx32G" CreateSomaticPanelOfNormals \
	-vcfs $l \
	-O ${p}.pon.vcf.gz
