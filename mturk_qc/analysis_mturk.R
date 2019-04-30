# Author: Alicia Parrish
# Created Spring 2019
# Script for analyzing mturk data

library(dplyr)
library(tidyr)
library(ggplot2)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

filenames = list.files("batch_results/", pattern='*.sv',full.names = T)

# loop through and merge all the data files needed
allData=NULL
for(i in c(1:length(filenames))){
  temp = read.csv(filenames[i],header=F)
  allData = rbind(allData,temp)
}

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
                                 answer > 3  ~ 1))%>%
  mutate(environment=case_when(environment=="sentential_negation_biclausal" ~ "Sent-neg",
                                  environment =="determiner_negation_biclausal" ~ "Det-neg",
                                  environment == "simplequestions" ~ "simp-Q",
                                  environment == "superlative" ~ "super",
                                  TRUE ~ environment))%>%
  mutate_at(vars(acceptable),funs(as.factor))

means <- Data4 %>% 
  group_by(environment,npi,acceptable) %>% 
  summarise(rating = mean(binary_answer),count=n())

all_means <- Data4 %>% 
  group_by(environment,npi,licensor,scope,npi_present,acceptable) %>% 
  summarise(rating = mean(binary_answer),count=n())

(plot<-ggplot(means,aes(x=environment,y=rating))+
  geom_bar(aes(fill = acceptable),stat = "identity",position = "dodge")+
  facet_wrap(~npi))

detnegever<-Data4%>%
  filter(environment=="conditional",npi=="ever")

ggsave(filename = 'figures/binary_answer_prelim.jpg',plot,width=12,height=4)
