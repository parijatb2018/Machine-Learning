carData=read.csv("cardata.csv")

summary(carData)
str(carData)

library(caTools)

set.seed(5580)

split= sample.split(carData$shouldBuy, SplitRatio = 0.75)
train= subset(carData, split == TRUE)
test= subset(carData, split == FALSE)

x_train=train[,1:6]
y_train=train[,7]

x_test=test[,1:6]
y_test=test[,7]

# Try rpart 
library(rpart)
carTree = rpart(shouldBuy~.,data=train,method="class",control=rpart.control(minsplit=1))
#carTree = rpart(Play~.,data=train,method="class",control=rpart.control(minsplit=5))
carTree

predCar=predict(carTree,newdata=test[,-7],type="class")

treeCM=table(test[,7],predCar)
treeCM
sum(diag(treeCM))/sum(treeCM)

library(rpart.plot)
rpart.plot(carTree)
prp(carTree)



# RF with ntree=500

#install.packages("randomForest")

library(randomForest)

rf=randomForest(x_train,y_train,ntree=500)

rfp=predict(rf,x_test)

combo2=cbind(rfp, y_test)

combo2

rfCM=table(rfp,y_test)
rfCM
sum(diag(rfCM))/sum(rfCM)
s<-sum(diag(rfCM))/sum(rfCM)

#install.packages("pROC")
library(pROC)
rfProb=predict(rf,x_test,type="prob")

rfProb

r1<- roc(y_test,rfProb[,1])

auc1<-auc(r1)

x1<-paste("RandonForest:ntree=500",",","AUC= ",round(auc1,6),",","Accuracy=",round(s,5))

plot(r1,main=x1)

# RF with ntree=50#
rf=randomForest(x_train,y_train,ntree=50)
rfp=predict(rf,x_test)
rfCM=table(rfp,y_test)
rfCM
sum(diag(rfCM))/sum(rfCM)
s<-sum(diag(rfCM))/sum(rfCM)

rfProb=predict(rf,x_test,type="prob")

roc(y_test,rfProb[,1])
plot(roc(y_test,rfProb[,1]))

r2<- roc(y_test,rfProb[,1])

auc2<-auc(r2)

x2<-paste("RandonForest:ntree=50",",","AUC= ",round(auc2,6),",","Accuracy=",round(s,5))

plot(r1,main=x2)

roc.test(r1,r2)

# RF, ntree=10#
rf=randomForest(x_train,y_train,ntree =10)
rfp=predict(rf,x_test)
rfCM=table(rfp,y_test)
rfCM
sum(diag(rfCM))/sum(rfCM)
s<-sum(diag(rfCM))/sum(rfCM)
rfProb=predict(rf,x_test,type="prob")

roc(y_test,rfProb[,1])
plot(roc(y_test,rfProb[,1]))

r3<- roc(y_test,rfProb[,1])

auc3<-auc(r3)

x3<-paste("RandonForest:ntree=10",",","AUC= ",round(auc3,6),",","Accuracy=",round(s,5))

plot(r3,main=x3)

# RF with 10 fold cross validation,ntree=500
library(caret)
library(ggplot2)
library(e1071)

metric <- "Accuracy"

control <- trainControl(method="repeatedcv", number=10, repeats=3)

rf_default <- train(x_train,y_train, method="rf", metric=metric, trControl=control,ntree=500)

rfp=predict(rf_default,x_test)
rfCM=table(rfp,y_test)
rfCM
sum(diag(rfCM))/sum(rfCM)
s<-sum(diag(rfCM))/sum(rfCM)
print(rf_default)

rfProb=predict(rf_default,x_test,type="prob")

roc(y_test,rfProb[,1])
plot(roc(y_test,rfProb[,1]))

r4<- roc(y_test,rfProb[,1])

auc4<-auc(r4)

x4<-paste("RandonForest/10-fold cross validation:ntree=500",",","AUC= ",round(auc4,6),",","Accuracy=",round(s,5))
plot(r4,main=x4)

varImp(rf_default)

ggplot(varImp(rf_default))