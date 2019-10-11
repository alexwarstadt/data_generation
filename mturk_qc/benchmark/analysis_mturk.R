# Author: Alicia Parrish
# Created Summer 2019
# Script for pulling analyzing human validation of Benchmark

library(dplyr)
library(tidyr)
library(rjson)
library(stringr)
library(ggplot2)

setwd("~/data_generation/mturk_qc/benchmark")

############### 
# assign qualification to mturkers who've already taken the survey
file<-read.csv("raw_results/Batch_3792952_batch_results.csv",header=T,check.names=FALSE)

allNewWorkers<-data.frame("WorkerId"=unique(file$WorkerId))
workers<-allNewWorkers%>%mutate("UPDATE-BLiMP"=1)

write.csv(workers,"workerfile_BLiMP_2.csv",na="",row.names=F)
###############

filenames = list.files("raw_results/", pattern='*.csv',full.names = T)

# loop through and merge all the data files needed
allData=NULL
for(i in c(1:length(filenames))){
  temp = read.csv(filenames[i],header=T)
  # I changed a variable name partway through. whoops.
  if("Answer.humans" %in% names(temp)){
    temp = temp %>% mutate("Answer.humans_math"=NA, "Answer.humans_text"=NA)
  } else if("Answer.humans_math" %in% names(temp)){
    temp = temp %>% mutate("Answer.humans"=NA)
  }
  allData = rbind(allData,temp)
}

anonCode<-c(1:length(unique(allData$WorkerId)))
anons<-data.frame(anonCode=anonCode,
                  WorkerId=unique(allData$WorkerId))
withAnonCode<-merge(allData,anons,by="WorkerId")

seeIds<-withAnonCode%>%
  group_by(WorkerId)%>%
  summarise(count=n())

anonymizedData<-withAnonCode%>%
  select(-WorkerId)

# save anonymized here
write.csv(anonymizedData,"anonymizedData_BLiMP_final.csv",row.names=F)

meanWorkTime=mean(allData$WorkTimeInSeconds,na.rm=T)
sdWorkTime=sd(allData$WorkTimeInSeconds,na.rm=T)

Data1<-allData%>%
  filter(AssignmentStatus!="Rejected")%>%
  filter(Answer.english==1)%>%
  #filter(WorkTimeInSeconds>30)%>%
  mutate(full1=paste(Input.item_1_condition,"--",Input.field_1_1,"--",Input.field_1_2,"--",Answer.Choice1))%>%
  mutate(full2=paste(Input.item_2_condition,"--",Input.field_2_1,"--",Input.field_2_2,"--",Answer.Choice2))%>%
  mutate(full3=paste(Input.item_3_condition,"--",Input.field_3_1,"--",Input.field_3_2,"--",Answer.Choice3))%>%
  mutate(full4=paste(Input.item_4_condition,"--",Input.field_4_1,"--",Input.field_4_2,"--",Answer.Choice4))%>%
  mutate(full5=paste(Input.item_5_condition,"--",Input.field_5_1,"--",Input.field_5_2,"--",Answer.Choice5))%>%
  select(Input.answer_order,Input.list,
         full1,full2,full3,full4,full5)%>%#,
         #Answer.native,Answer.navtive)%>%
  gather(setNum,allInfo,-Input.answer_order,-Input.list)%>%#,-Answer.native,-Answer.navtive)
  separate(allInfo,c("Condition","Sentence1","Sentence2","Answer"),"--",remove=F)%>%
  mutate(eachSent=paste0(Condition,Sentence1))%>%
  filter(!Condition%in%c("attnchkans1 ","attnchkans2 "))%>%
  filter(Answer!=" NA")%>%
  mutate(corrResp=as.numeric(str_sub(Condition,start=-2,end=-1)))%>%
  mutate(answerGiven=as.numeric(str_sub(Answer,start=2,end=2)))%>%
  mutate(is.corr=ifelse(corrResp==answerGiven, TRUE, FALSE))%>%
  mutate(Condition=str_sub(Condition,start=1,end=-6))%>%
  filter(Condition!="subject_island")%>%
  filter(!is.na(is.corr))

(plot=ggplot()+
    geom_bar(data=Data1, aes(x=Condition,fill=is.corr))+
    theme(axis.text.x = element_text(angle = 50, hjust = 1)))

# get by sent means
Data2<-Data1%>%
  mutate(numeric_answer=case_when(is.corr == TRUE ~ 1,
                                is.corr == FALSE  ~ 0))%>%
  group_by(eachSent,Condition)%>%
  summarise(rating=mean(numeric_answer),count=n())%>%
  mutate(good_sent=case_when(rating>0.5~1,
                             rating<=0.5~0))%>%
  group_by(Condition)%>%
  summarise(accepted=sum(good_sent))
