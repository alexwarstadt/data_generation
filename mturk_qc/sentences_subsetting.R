# Author: Alicia Parrish
# Script for pulling a random sentence from each condition for mturk validation

library(dplyr)
library(tidyr)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

filenames = list.files("../outputs/npi/environments/", pattern='*.tsv',full.names = T)
allData=NULL
for(i in c(1:length(filenames))){
  temp = read.table(filenames[i],sep='\t',header=F)
  allData = rbind(allData,temp)
}

# make tsv with all environments
# write.table(allData,"../outputs/npi/all_environments.tsv",sep='\t',col.names=NA)

names(allData) <- c('metadata','acceptability','blank','sentence')

smaller = function(x) (gsub(".*=","",x))

# separate conditions and randomize
Data2 = allData%>%
  select(-blank)%>%
  separate(metadata,c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),"-",remove=F)%>%
  mutate_at(c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),smaller)%>%
  mutate(rand_int=round(runif(nrow(allData),min=0,max=100000)))%>%
  arrange(rand_int)

# subset to only 'ever' and 'any'
Data3<-Data2%>%
  filter(npi=='ever'|npi=='any')

# should give 136 rows each
examples1 = Data3[!duplicated(Data3[c("experiment","environment","npi","licensor","scope","npi_present")]),]

Data4<-Data3 %>% filter(!metadata %in% examples$metadata)
examples2 <- Data4[!duplicated(Data4[c("experiment","environment","npi","licensor","scope","npi_present")]),]

Data5<-Data4 %>% filter(!metadata %in% examples2$metadata)
examples3 <- Data5[!duplicated(Data5[c("experiment","environment","npi","licensor","scope","npi_present")]),]

# oversample from everything except sentential neg, determiner neg, only cases +80
Data6<- Data5 %>% filter(environment!='sentential_negation_biclausal',
                         environment!='determiner_negation_biclausal',
                         environment!='only',
                         !metadata %in% examples3$metadata)
examples4<-Data6[!duplicated(Data6[c("experiment","environment","npi","licensor","scope","npi_present")]),]

# take 4 more random rows to make an even set
Data7<-Data6 %>% filter(!metadata %in% examples4$metadata)
examples_to_subset<-Data7[!duplicated(Data7[c("experiment","environment","npi","licensor","scope","npi_present")]),]
examples5<-examples_to_subset[1:4,]

# should be 500 rows
all_examples<-rbind(examples1,examples2,examples3,examples4,examples5)

# check for no duplicates in metadata --> should be 0
nrow(all_examples[duplicated(all_examples["metadata"]),])

# check for no duplicates in metadata --> should be 500
length(unique(all_examples$metadata))

# sanity check 
see_env<-all_examples%>%
  group_by(environment)%>%
  summarise(count=n())

# sanity check that I'm pulling random paradigms
see<-all_examples %>%
  group_by(paradigm)%>%
  summarise(count=n())

write.table(all_examples,"examples.tsv", sep='\t',col.names=NA)

#--------------
# separate into smaller datasets of 4 sentences each

examples_rand=all_examples%>%
  mutate(metadata=paste0(metadata,"-acceptability=",acceptability))%>%
  mutate(rand_int=round(runif(nrow(all_examples),min=0,max=100000)))%>%
  arrange(rand_int)

attnChks = read.table("attention_checks.txt",sep='\t',header=T)

already_used = NULL
FullTurkDataset = NULL
for(i in c(1:125)){
  newData = examples_rand%>%
    filter(!metadata%in%already_used$metadata)
  tempData = newData[!duplicated(newData[c("environment","npi")]),]
  print(paste0("tempData run",i,": ",nrow(tempData)))
  if(nrow(tempData)>=4){
    subsetTempData = tempData[1:4,]
  } else {
    print(paste0("using newData, run",i,": ",nrow(newData)))
    subsetTempData = newData[1:4,] 
  }
  print(paste0("subsetTempData run",i,": ",nrow(subsetTempData)))
  print(paste0("accpetability of items in run ",i,": ",subsetTempData$acceptability))
  already_used = rbind(already_used,subsetTempData)
  dataFile = rbind(subsetTempData,attnChks)
  cond1 = as.character(dataFile$metadata[1])
  cond2 = as.character(dataFile$metadata[2])
  cond3 = as.character(dataFile$metadata[3])
  cond4 = as.character(dataFile$metadata[4])
  cond_attn = as.character(dataFile$metadata[5])
  sent1 = as.character(dataFile$sentence[1])
  sent2 = as.character(dataFile$sentence[2])
  sent3 = as.character(dataFile$sentence[3])
  sent4 = as.character(dataFile$sentence[4])
  sent_attn = as.character(dataFile$sentence[5])
  turkDataFile <- data.frame('list' = c(1:4),
                           'item_1_condition'= c(cond1,cond2,cond3,cond4), #1243
                           'field_1_1'= c(sent1,sent2,sent3,sent4),
                           'item_2_condition' = c(cond2,cond3,cond1,cond4), #2314
                           'field_2_1'= c(sent2,sent3,sent1,sent4),
                           'item_3_condition' = c(cond3,cond4,cond2,cond1), #3421
                           'field_3_1'= c(sent3,sent4,sent2,sent1),
                           'item_4_condition' = c(cond_attn,cond_attn,cond_attn,cond_attn), # attn chks
                           'field_4_1' = c(sent_attn,sent_attn,sent_attn,sent_attn),
                           'item_5_condition' = c(cond4,cond1,cond3,cond2), #4132
                           'field_5_1' = c(sent4,sent1,sent3,sent2))
  FullTurkDataset=rbind(FullTurkDataset,turkDataFile)
}

# give unique identifier to each list
FullTurkDataset$list<-seq.int(nrow(FullTurkDataset))

# sanity check --> should give 500
length(unique(FullTurkDataset$item_5_condition))
# sanity check --> should give 1
length(unique(FullTurkDataset$item_4_condition))

write.csv(FullTurkDataset,"mturk_dataset.csv",row.names=F)

