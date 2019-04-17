# Author: Alicia Parrish
# Script for pulling a random sentence from each condition for mturk validation

library(dplyr)
library(tidyr)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

allData = read.table('../outputs/npi/all_environments.tsv',sep='\t',header=F)
names(allData) <- c('metadata','acceptability','blank','sentence')

smaller = function(x) (gsub(".*=","",x))

# separate conditions and randomize
Data2 = allData%>%
  select(-blank)%>%
  separate(metadata,c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),"-",remove=F)%>%
  mutate_at(c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm"),smaller)%>%
  mutate(rand_int=round(runif(nrow(Data2),min=0,max=100000)))%>%
  arrange(rand_int)

# troubleshotting
nopara = function(x) (gsub("para.*","",x))
simpQs<-allData%>%
  filter(grepl("simplequestions",metadata))%>%
  mutate(metadata=nopara(metadata))

# should give 400 rows  
examples = Data2[!duplicated(Data2[c("experiment","environment","npi","licensor","scope","npi_present")]),]

# sanity check 
see_env<-examples%>%
  group_by(environment)%>%
  summarise(count=n())

# another sanity check
see_neg<-examples%>%
  filter(environment=="negation")

# more sanity checking
see_simpQ<-Data2%>%
  filter(environment=="simplequestions")

# sanity check that I'm pulling random paradigms
see<-examples %>%
  group_by(paradigm)%>%
  summarise(count=n())

# oversample from adverb cases +40 items
more_adverbs = Data2 %>%
  filter(environment == 'adverbs')%>%
  filter(!metadata%in%examples$metadata)
more_adverb_examples = more_adverbs[!duplicated(more_adverbs[c("npi","licensor","scope","npi_present")]),]

# oversample from superlative cases +48
more_supers = Data2 %>%
  filter(environment == 'superlative')%>%
  filter(!metadata%in%examples$metadata)
more_super_examples = more_supers[!duplicated(more_supers[c("npi","licensor","scope","npi_present")]),]

# pull an extra random 12 cases, so total number will =500 examples
more_sentence_items = Data2 %>%
  filter(!metadata%in%more_adverb_examples$metadata)%>%
  filter(!metadata%in%more_super_examples$metadata)%>%
  filter(!metadata%in%examples$metadata)
more_sentences = more_sentence_items[!duplicated(more_sentence_items[c("npi","licensor","scope","npi_present")]),]
more_sentence_examples = more_sentences[1:12,]

# this should equal 500 items
examples_full = rbind(more_adverb_examples,more_super_examples,more_sentence_examples,examples)

#check for no duplicates in metadata --> should be 500 in the output.
length(unique(examples_full$metadata))

write.table(examples_full,"examples.tsv", sep='\t',col.names=NA)

#--------------
# separate into 25 smaller datasets

examples_rand=examples_full%>%
  mutate(rand_int=round(runif(nrow(examples_full),min=0,max=100000)))%>%
  arrange(rand_int)
examples=examples_rand[1:500,]

attnChks = read.table("attention_checks.txt",sep='\t',header=T)
  
already_used = NULL
for(i in c(1:25)){
  newData = examples%>%
    filter(!metadata%in%already_used$metadata)
  tempData = newData[!duplicated(newData[c("environment","npi")]),]
  print(paste0("tempData run",i,": ",nrow(tempData)))
  if(nrow(tempData)>=20){
    subsetTempData = tempData[1:20,]
  } else {
    print(paste0("using newData, run",i,": ",nrow(newData)))
    subsetTempData = newData[1:20,] 
  }
  print(paste0("subsetTempData run",i,": ",nrow(subsetTempData)))
  already_used = rbind(already_used,subsetTempData)
  dataFile = rbind(subsetTempData,attnChks)
  write.table(dataFile,paste0("dataset",i,".tsv"), sep='\t',col.names=NA)
}

# check last dataset
see25=read.table("dataset25.tsv",sep='\t',header=T)
