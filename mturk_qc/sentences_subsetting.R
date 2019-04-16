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
  mutate(rand_int=round(runif(nrow(Data2),min=0,max=100000)))%>%
  arrange(rand_int)

# should give 452 rows  
examples = Data2[!duplicated(Data2[c("experiment","environment","npi","licensor","scope","npi_present")]),]

# sanity check that I'm pulling random paradigms
see<-examples %>%
  group_by(paradigm)%>%
  summarise(count=n())

write.table(examples,"examples.tsv",quote=FALSE, sep='\t',col.names=NA)

#--------------
# separate into 25 smaller datasets

already_used = NULL
for(i in c(1:25)){
  newData = examples%>%
    filter(!paradigm%in%already_used$paradigm)%>%
    select(-blank)
  tempData = newData[!duplicated(Data2[c("environment","npi")]),]
  if(i==1 | i==2){
    subsetTempData = tempData[1:19,]
  } else {
    subsetTempData = tempData[1:18,]
  }
  already_used = rbind(already_used,subsetTempData)
  write.table(subsetTempData,paste0("dataset",i,".tsv"),quote=FALSE, sep='\t',col.names=NA)
}
  
