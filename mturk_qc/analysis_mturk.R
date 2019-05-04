# Author: Alicia Parrish
# Created Spring 2019
# Script for analyzing mturk data

library(dplyr)
library(tidyr)
library(ggplot2)

setwd("G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/mturk_qc")

############### 
# assign qualification to mturkers who've already taken the survey
#workers<-read.csv("User_1164208_workers.csv",header=T,check.names=FALSE)
#newbatch<-read.csv("batch_results/Batch_3628704_batch_results.csv", header=T)

#allNewWorkers<-unique(newbatch$WorkerId)
#workers2<-workers%>%
  #mutate(`UPDATE-SemSem2`=ifelse(`Worker ID`%in%allNewWorkers,1,`UPDATE-SemSem2`))

#write.csv(workers2,"workerfile.csv",na="",row.names=F)
###############

filenames = list.files("batch_results/", pattern='*.sv',full.names = T)

# loop through and merge all the data files needed
allData=NULL
for(i in c(1:length(filenames))){
  temp = read.csv(filenames[i],header=T)
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
write.csv(anonymizedData,"anonymizedData.csv",row.names=F)
  
Data2<-anonymizedData%>%
  select(AssignmentId,anonCode,AssignmentStatus,Answer.english,
         Input.item_1_condition,Input.field_1_1,Answer.Choice1,
         Input.item_2_condition,Input.field_2_1,Answer.Choice2,
         Input.item_3_condition,Input.field_3_1,Answer.Choice3,
         Input.item_4_condition,Input.field_4_1,Answer.Choice4,
         Input.item_5_condition,Input.field_5_1,Answer.Choice5)

Data3<-Data2%>%
  filter(AssignmentStatus=="Approved",Answer.english==1)

smaller = function(x) (gsub(".*=","",x))

Data4<-Data3%>%
  mutate(full1=paste(Input.item_1_condition,"_Sentence=",Input.field_1_1,"_AnswerChoice=",Answer.Choice1))%>%
  mutate(full2=paste(Input.item_2_condition,"_Sentence=",Input.field_2_1,"_AnswerChoice=",Answer.Choice2))%>%
  mutate(full3=paste(Input.item_3_condition,"_Sentence=",Input.field_3_1,"_AnswerChoice=",Answer.Choice3))%>%
  mutate(full4=paste(Input.item_4_condition,"_Sentence=",Input.field_4_1,"_AnswerChoice=",Answer.Choice4))%>%
  mutate(full5=paste(Input.item_5_condition,"_Sentence=",Input.field_5_1,"_AnswerChoice=",Answer.Choice5))%>%
  select(AssignmentId,anonCode,
         full1,full2,full3,full4,full5)%>%
  gather(setNum,allInfo,-AssignmentId,-anonCode)%>%
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
  mutate_at(vars(acceptable),funs(as.factor))%>%
  filter(!is.na(answer))

overaccept_any<-Data4%>%
  filter(npi=="any",acceptable==0,answer>3)

means <- Data4 %>% 
  group_by(environment,npi,acceptable) %>% 
  summarise(rating = mean(answer),count=n())

all_means <- Data4 %>% 
  group_by(environment,npi,licensor,scope,npi_present,acceptable) %>% 
  summarise(rating = mean(answer),count=n())

(plot<-ggplot(means,aes(x=environment,y=rating))+
  geom_bar(aes(fill = acceptable),stat = "identity",position = "dodge")+
    theme(axis.text.x = element_text(angle = 50, hjust = 1))+
  facet_wrap(~npi))

seeQuant<-Data4%>%
  filter(environment=="quantifier")%>%
  group_by(npi,licensor,crucial_item,scope,npi_present,acceptable) %>%
  summarise(rating = mean(binary_answer),count=n())

(plot2<-ggplot(seeQuant,aes(x=crucial_item,y=rating))+
    geom_bar(aes(fill = acceptable),stat = "identity",position = "dodge")+
    theme(axis.text.x = element_text(angle = 50, hjust = 1))+
    facet_wrap(~npi))

see-env<-Data4%>%
  filter(environment=="super",npi=="any")

just1cond<-Data4%>%
  filter(environment=="conditional")%>%
  group_by(npi,licensor,crucial_item,scope,npi_present,acceptable) %>%
  summarise(rating = mean(binary_answer),count=n())

(plot3<-ggplot(just1cond,aes(x=npi,y=rating))+
    geom_bar(aes(fill = acceptable),stat = "identity",position = "dodge")+
    theme(axis.text.x = element_text(angle = 50, hjust = 1))+
    facet_wrap(~licensor*scope*npi_present))

means_by_sent<-Data4%>%
  group_by(environment,npi,licensor,scope,npi_present,acceptable,sentence)%>%
  summarise(rating=mean(answer),count=n())%>%
  mutate(binary_answer=case_when(rating <= 3.5 ~ 0,
                                 rating > 3.5  ~ 1))%>%
  group_by(environment,npi,acceptable)%>% 
  summarise(rating1 = mean(binary_answer),count=n())

means_by_sent_binary<-Data4%>%
  mutate(binary_resp=case_when(answer <= 3.5 ~ 0,
                                 answer > 3.5  ~ 1))%>%
  group_by(environment,npi,licensor,scope,npi_present,acceptable,sentence)%>%
  summarise(rating=mean(binary_resp),count=n())%>%
  mutate(binary_answer=case_when(rating <= .5 ~ 0,
                                 rating > .5  ~ 1))%>%
  group_by(environment,npi,acceptable)%>% 
  summarise(rating1 = mean(binary_answer),count=n())

(plot4<-ggplot(means_by_sent,aes(x=environment,y=rating1))+
    geom_bar(aes(fill = acceptable),stat = "identity",position = "dodge")+
    theme(axis.text.x = element_text(angle = 50, hjust = 1))+
    facet_wrap(~npi))

ggsave(filename = 'figures/binary_answer_prelim.jpg',plot,width=12,height=4)

write.table(all_means,"prelim_data_means.tsv", sep='\t')

#############################
# t-tests

all_envs<-unique(Data4$environment)
NPIs<-unique(Data4$npi)

test_values=NULL
for(environ in all_envs){
  for(npi1 in NPIs){
    thisData<-Data4%>%
      filter(environment==environ,npi==npi1)
    test=wilcox.test(data=thisData, binary_answer~acceptable) 
    add_test=data.frame(NPI=npi1,
                        environment=environ,
                        w=test[1],
                        p.value=test[3],
                        mean0=mean(thisData$binary_answer[thisData$acceptable==0]),
                        mean1=mean(thisData$binary_answer[thisData$acceptable==1])
    )
    test_values=rbind(add_test,test_values)
  }
}

write.csv(test_values,"wilcox_test_binary_rating.csv",row.names=F)
