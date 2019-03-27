#install.packages("doMC")
#library(doMC)
#registerDoMC(4)
library(caret)
#
xy=read.table("p1.csv",sep=',',header=F)
y=xy[,8]
head(y)
x=xy[,1:7]

# Using pre-sliced data
myCvControl <- trainControl(method = "repeatedCV",
                            number=10,
                            repeats = 5)

# Linear regression
glmFitTime <- train(V8 ~ .,
                    data = xy,
                    method = "glm",
                    preProc = c("center", "scale"),
                    tuneLength = 10,
                    trControl = myCvControl)
glmFitTime
summary(glmFitTime)
y_hat = predict(glmFitTime, newdata = x)
mean(100*abs(y_hat-y)/y) #Mean Absolute Percentage Error
# Your error with linear regression

# Support Vector Regression
svmFitTime <- train(V8 ~ .,
                    data = xy,
                    method = "svmRadial",
                    preProc = c("center", "scale"),
                    tuneLength = 10,
                    trControl = myCvControl)
svmFitTime
summary(svmFitTime)
y_hat = predict(svmFitTime, newdata = x)
mean(100*abs(y_hat-y)/y)
# Your error with support vector regression

# Neural Network
nnFitTime <- train(V8 ~ .,
                   data = xy,
                   method = "avNNet",
                   preProc = c("center", "scale"),
                   trControl = myCvControl,
                   tuneLength = 10,
                   linout = T,
                   trace = F,
                   MaxNWts = 10 * (ncol(xy) + 1) + 10 + 1,
                   maxit = 500)
nnFitTime
summary(nnFitTime)
y_hat = predict(nnFitTime, newdata = x)
mean(100*abs(y_hat-y)/y)
# Your error with neural networks

# You can experiment with other methods, here is where you can find the methods caret supports:
# https://topepo.github.io/caret/available-models.html

# Compare models
resamps <- resamples(list(lm = glmFitTime,
                          svn = svmFitTime,
                          nn = nnFitTime))
summary(resamps)


# Now working with the time-series modeling

#t=read.table("timeSeries.txt",header=F)
t=read.table("p1t.csv",sep=',',header=F)
head(t)
tSeries = ts(t[,3],start=1,freq=7)
length(tSeries)
head(tSeries, n=20)

plot(tSeries)
#ltseries<-log(tSeries)
#head(ltseries)
#plot(ltseries)
#plot(stl(ltseries,s.window="periodic"))

plot(stl(tSeries,s.window="periodic"))


#install.packages("forecast")
#install.packages('tseries') 
library('tseries')
#install.packages("forecast", dependencies = TRUE)
library("forecast")

hw = ets(tSeries,model="MAM")
mean(100*abs(fitted(hw) - tSeries)/tSeries)
# Your Holt-Winters error

fitted(hw)

hw1=HoltWinters(tSeries)

hw1$fit[1:10]
tSeries[1:10]

ar <- Arima(tSeries,order=c(7,0,7))
#ar <- arima(tSeries,order=c(7,0,7))
mean(100*abs(fitted(ar) - tSeries)/tSeries)

t1=read.table("p2t.csv",sep=',',header=F)
head(t)
tSeries1 = ts(t[,3],start=1,freq=7)
ar1 <- Arima(tSeries1,model=ar)

fitted(ar1)

mean(100*abs(fitted(ar1) - tSeries1)/tSeries1)

xx<-predict(ar,n.ahead = 7)
print(xx)
# Your Arima error