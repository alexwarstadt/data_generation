# Author: Alicia Parrish
# Created Spring 2019
# Script for analyzing mturk data

library(dplyr)
library(tidyr)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

Data=read.csv("batch_results/Batch_3623659_batch_results.csv",header=T)

Data2<-Data%>%
  select(AssignmentId,WorkerId,AssignmentStatus,Answer.english,
         Input.item_1_condition,Input.field_1_1,Answer.Choice1,
         Input.item_2_condition,Input.field_2_1,Answer.Choice2,
         Input.item_3_condition,Input.field_3_1,Answer.Choice3,
         Input.item_4_condition,Input.field_4_1,Answer.Choice4,
         Input.item_5_condition,Input.field_5_1,Answer.Choice5)
Data3<-Data2%>%
  filter(AssignmentStatus!="Rejected",Answer.english==1)

smaller = function(x) (gsub(".*=","",x))

Data4<-Data3%>%
  mutate(full1=paste(Input.item_1_condition,"_Sentence=",Input.field_1_1,"_AnswerChoice=",Answer.Choice1))%>%
  mutate(full2=paste(Input.item_2_condition,"_Sentence=",Input.field_2_1,"_AnswerChoice=",Answer.Choice2))%>%
  mutate(full3=paste(Input.item_3_condition,"_Sentence=",Input.field_3_1,"_AnswerChoice=",Answer.Choice3))%>%
  mutate(full4=paste(Input.item_4_condition,"_Sentence=",Input.field_4_1,"_AnswerChoice=",Answer.Choice4))%>%
  mutate(full5=paste(Input.item_5_condition,"_Sentence=",Input.field_5_1,"_AnswerChoice=",Answer.Choice5))%>%
  select(AssignmentId,WorkerId,
         full1,full2,full3,full4,full5)%>%
  gather(setNum,allInfo,-AssignmentId,-WorkerId)%>%
  filter(setNum!="full4")%>%
  separate(allInfo,c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm","acceptability"),"-",remove=F)%>%
  separate(acceptability,c("acceptable","sentence","answer"),"_")%>%
  mutate_at(c("experiment","environment","npi","crucial_item","licensor","scope","npi_present","paradigm","acceptable","sentence","answer"),smaller)%>%
  rename("metadata"=allInfo)%>%
  mutate_at(vars(acceptable,answer),funs(as.numeric))%>%
  mutate(binary_answer=case_when(answer <= 3 ~ 0,
                                 answer > 3  ~ 1))

means <- Data4 %>% 
  group_by(environment,npi,acceptable) %>% 
  summarise(rating = mean(binary_answer))

