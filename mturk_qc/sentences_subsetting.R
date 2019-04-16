# Author: Alicia Parrish
# Script for pulling a random sentence from each condition for mturk validation

library(dplyr)
library(tidyr)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

allData = read.table('../outputs/npi/all_environments.tsv',sep='\t',header=F)
names(allData) <- c('metadata','acceptability','blank','sentence')

smaller = function(x) (gsub(".*=","",x))

Data2 = allData%>%
  separate(metadata,c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),"-")%>%
  mutate_at(c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),smaller)%>%
  mutate(rand_int=round(runif(nrow(Data2),min=0,max=10000)))%>%
  arrange(rand_int)

# should give 452 rows  
examples = Data2[!duplicated(Data2[c("experiment","environment","npi","licensor","scope","npi_present")]),]

write.table(examples,"examples2.tsv",quote=FALSE, sep='\t',col.names=NA)
