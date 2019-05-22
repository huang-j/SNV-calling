#!/usr/bin/env Rscript
library(deconstructSigs)
library(data.table)
library(dplyr)


args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied.n", call.=FALSE)
} else if (length(args) == 1) {
  args[2] = "annotated"
}
dn <- dirname(args[1])
sample <- basename(args[1])
sample <- unlist(strsplit(sample, "[.]"))[1]
if (args[2] == "VCF") {
  samp <- fread(args[1], skip="130", sep="\t") 
  df <- data.frame(sample=c(rep("samp", samp[,.N])),
                   chr=samp$`#CHROM`,
                   pos=samp$POS,
                   ref=samp$REF,
                   alt=samp$ALT
                   )
} else {
  samp <- fread(args[1], sep="\t")
  df <- data.frame(sample=c(rep("samp", samp[, .N])),
                   chr=samp$Chr,
                   pos=samp$Start,
                   ref=samp$Ref,
                   alt=samp$Alt
                   )
}

smpins <- mut.to.sigs.input(mut.ref=df,
                            sample.id="sample",
                            chr="chr",
                            ref="ref",
                            alt="alt"
                            )

smpout <- whichSignatures(tumor.ref=smpins,
                          signatures.ref = signatures.cosmic,
                          contexts.needed=TRUE,
                          tri.counts.method = "default")
weights <- transpose(smpout$weights)
rownames(weights) <- colnames(smpout$weights)
write.table(weights, paste0(dn, "/", sample, ".signature.tsv"), sep="\t",quote = FALSE)
png(filename = paste0(dn,"/",sample,".signature.png"), width = 1600, height = 1800, units="px", res = 250)
plotSignatures(smpout)
dev.off()
