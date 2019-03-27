#Set up of files and libraries
#install.packages("arules")
library("arules")
tr=read.transactions('user2.csv',format="basket",sep=",")

# Exploratory analysis
summary(tr)
itemFrequencyPlot(tr,topN=10)

####User analysis###
#Parameter tuning
rules<- apriori(tr, parameter= list(supp=0.2, conf=0.5))# too many rules
rules<- apriori(tr, parameter= list(supp=0.3, conf=0.5))
rules<- apriori(tr, parameter= list(supp=0.4, conf=0.5))#very less rules

#Final model 
rules<- apriori(tr, parameter= list(supp=0.3, conf=0.5))
#inspect(rules)

inspect(sort(rules,by='lift'))
inspect(sort(rules,by='lift')[1:15])

#Itemsets
itemsets=unique(generatingItemsets(rules))
#itemsets=(generatingItemsets(rules))
write(itemsets)
summary(itemsets)
write(rules,file="userRules.txt")

#To get maximally frequent itemsets
maximal.sets<- apriori(tr, parameter= list(supp=0.3, conf=0.5, target="maximally frequent itemsets"))
write(maximal.sets)


### Session level analysis
tr=read.transactions("user5.csv",format="basket",sep=",")
#Parameter tuning

rules<- apriori(tr, parameter= list(supp=0.3, conf=0.5))# less rules
rules<- apriori(tr, parameter= list(supp=0.2, conf=0.5))
rules<- apriori(tr, parameter= list(supp=0.1, conf=0.5))#too many rules

# Final model 
rules<- apriori(tr, parameter= list(supp=0.2, conf=0.5))
inspect(sort(rules,by='lift'))

#Itemsets
itemsets=unique(generatingItemsets(rules))
write(rules,file="sessionRules.txt")

#To get maximally frequent itemsets
maximal.sets<- apriori(tr, parameter= list(supp=0.2, conf=0.5, target="maximally frequent itemsets"))
write(maximal.sets)