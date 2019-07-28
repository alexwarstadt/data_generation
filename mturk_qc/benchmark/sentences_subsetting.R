# Author: Alicia Parrish
# Created Summer 2019
# Script for pulling 5 random sentence pairs from each paradigm for mturk validation

library(dplyr)
library(tidyr)
library(rjson)

setwd("~/data_generation/mturk_qc/benchmark")

filenames = list.files("../../outputs/benchmark/", pattern='*.jsonl',full.names = T)

# loop through and merge all the data files needed
selectData=NULL
allData=NULL
for(i in c(1:length(filenames))){
  temp1 = data.frame(Reduce(rbind, lapply(readLines(filenames[i]), fromJSON)))
  temp2 = temp1 %>%
    select(sentence_good, sentence_bad, UID) %>%
    unnest()
  allData = rbind(allData,temp2)
  select = temp2[1:5,]
  selectData = rbind(selectData,select)
}

# save a file of unformated examples to be validated
write.table(selectData,"all_data_to_validate.tsv", sep='\t',col.names=NA)

#--------------

# randomize
examples_rand=selectData%>%
  mutate(rand_int=round(runif(nrow(selectData),min=0,max=100000)))%>%
  mutate(uniques=paste0(rand_int,UID))%>%
  arrange(rand_int)

# must be same as the number of observations
# length(unique(examples_rand$uniques))

# initialize data frame needed in the loop
already_used = NULL
FullTurkDataset = NULL

# read in attention check data file.
attnChks = read.csv("attention_checks.csv",header=T)

number_to_make=nrow(examples_rand)/4
# loop for formatting for turkTools -- make sure examples_rand has obs%%4==0
for(i in c(1:number_to_make)){
  # make sure used items are taken out
  newData = examples_rand%>%
    filter(!uniques%in%already_used$uniques)
  # get nonduplicates of minimal pair type
  tempData = newData[!duplicated(newData[c("UID")]),]
  #print(paste0("tempData run",i,": ",nrow(tempData)))
  # just in case the nonduplicates is less than 4, can pull from the full dataset
  if(nrow(tempData)>=4){
    subsetTempData = tempData[1:4,]
  } else {
    print(paste0("using newData, run",i,": ",nrow(newData)))
    subsetTempData = newData[1:4,] 
  }
  #print(paste0("subsetTempData run",i,": ",nrow(subsetTempData)))
  # add the selected 5 rows to already_used so they can be taken out on the next run of the loop
  already_used = rbind(already_used,subsetTempData)
  # add attention check item to the data
  chk = (i %% 4) + 1
  print(paste0("chk: ",chk))
  #dataFile = rbind(subsetTempData,attnChks[chk,])
  dataFile = subsetTempData
  # initialize variables that will need to be in the output
  cond1 = as.character(dataFile$uniques[1])
  cond2 = as.character(dataFile$uniques[2])
  cond3 = as.character(dataFile$uniques[3])
  cond4 = as.character(dataFile$uniques[4])
  #cond_attn = as.character(dataFile$uniques[5])
  #cond5 = as.character(dataFile$uniques[6])
  sent1.1 = as.character(dataFile$sentence_good[1])
  sent2.1 = as.character(dataFile$sentence_good[2])
  sent3.1 = as.character(dataFile$sentence_good[3])
  sent4.1 = as.character(dataFile$sentence_good[4])
  #sent_attn.1 = as.character(dataFile$sentence_good[5])
  #sent5.1 = as.character(dataFile$metadata_good[6])
  sent1.0 = as.character(dataFile$sentence_bad[1])
  sent2.0 = as.character(dataFile$sentence_bad[2])
  sent3.0 = as.character(dataFile$sentence_bad[3])
  sent4.0 = as.character(dataFile$sentence_bad[4])
  #sent_attn.0 = as.character(dataFile$sentence_bad[5])
  #sent5.0 = as.character(dataFile$metadata_bad[6])
  # create a dataframe with all conditions 
  if(chk==1){  # order 1: 1,2,2,1
    turkDataFile <- data.frame('answer_order' = c(chk),
                             'item_1_condition'= c(cond1), 
                             'field_1_1'= c(sent1.1),
                             'field_1_2'= c(sent1.0),
                             'item_2_condition' = c(cond2), 
                             'field_2_1'= c(sent2.0),
                             'field_2_2'= c(sent2.1),
                             'item_3_condition' = c(cond3), 
                             'field_3_1'= c(sent3.0),
                             'field_3_2'= c(sent3.1),
                             'item_4_condition' = c(cond4), 
                             'field_4_1' = c(sent4.1),
                             'field_4_2'= c(sent4.0)#,
                             #'item_5_condition' = c(cond_attn), 
                             #'field_5_1' = c(cond_attn),
                             #'field_5_2'= c(cond_attn),
                             #'item_6_condition' = c(cond5), 
                             #'field_6_1' = c(sent5),
                             #'field_6_2'= c(sent5)
                             )
  }
  if(chk==2){# order 1: 2,1,1,2
    turkDataFile <- data.frame('answer_order' = c(chk),
                               'item_1_condition'= c(cond1), 
                               'field_1_1'= c(sent1.0),
                               'field_1_2'= c(sent1.1),
                               'item_2_condition' = c(cond2), 
                               'field_2_1'= c(sent2.1),
                               'field_2_2'= c(sent2.0),
                               'item_3_condition' = c(cond3), 
                               'field_3_1'= c(sent3.1),
                               'field_3_2'= c(sent3.0),
                               'item_4_condition' = c(cond4), 
                               'field_4_1' = c(sent4.0),
                               'field_4_2'= c(sent4.1)#,
                               #'item_5_condition' = c(cond_attn), 
                               #'field_5_1' = c(cond_attn),
                               #'field_5_2'= c(cond_attn),
                               #'item_6_condition' = c(cond5), 
                               #'field_6_1' = c(sent5),
                               #'field_6_2'= c(sent5)
                              )
  }
  if(chk==3){# order 1: 1,2,1,2
    turkDataFile <- data.frame('answer_order' = c(chk),
                               'item_1_condition'= c(cond1), 
                               'field_1_1'= c(sent1.1),
                               'field_1_2'= c(sent1.0),
                               'item_2_condition' = c(cond2), 
                               'field_2_1'= c(sent2.0),
                               'field_2_2'= c(sent2.1),
                               'item_3_condition' = c(cond3), 
                               'field_3_1'= c(sent3.1),
                               'field_3_2'= c(sent3.0),
                               'item_4_condition' = c(cond4), 
                               'field_4_1' = c(sent4.0),
                               'field_4_2'= c(sent4.1)#,
                               #'item_5_condition' = c(cond_attn), 
                               #'field_5_1' = c(cond_attn),
                               #'field_5_2'= c(cond_attn),
                               #'item_6_condition' = c(cond5), 
                               #'field_6_1' = c(sent5),
                               #'field_6_2'= c(sent5)
                                )
  }
  if(chk==4){# order 1: 2,1,2,1
    turkDataFile <- data.frame('answer_order' = c(chk),
                               'item_1_condition'= c(cond1), 
                               'field_1_1'= c(sent1.0),
                               'field_1_2'= c(sent1.1),
                               'item_2_condition' = c(cond2), 
                               'field_2_1'= c(sent2.1),
                               'field_2_2'= c(sent2.0),
                               'item_3_condition' = c(cond3), 
                               'field_3_1'= c(sent3.0),
                               'field_3_2'= c(sent3.1),
                               'item_4_condition' = c(cond4), 
                               'field_4_1' = c(sent4.1),
                               'field_4_2'= c(sent4.0)#,
                               #'item_5_condition' = c(cond_attn), 
                               #'field_5_1' = c(cond_attn),
                               #'field_5_2'= c(cond_attn),
                               #'item_6_condition' = c(cond5), 
                               #'field_6_1' = c(sent5),
                               #'field_6_2'= c(sent5)
                                )
    }
  # add row to the full dataframe for mturk upload
  FullTurkDataset=rbind(FullTurkDataset,turkDataFile)
}

# give unique identifier to each list
FullTurkDataset$list<-seq.int(nrow(FullTurkDataset))

# sanity check --> should give TRUE
length(unique(FullTurkDataset$item_1_condition)) == round(number_to_make)
# sanity check --> these should all be false
duplicated(FullTurkDataset[1,])
duplicated(FullTurkDataset[2,])
duplicated(FullTurkDataset[3,])
duplicated(FullTurkDataset[4,])

write.csv(FullTurkDataset,"mturk_dataset.csv",row.names=F)
