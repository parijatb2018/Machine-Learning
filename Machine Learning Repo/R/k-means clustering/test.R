
library(ggplot2)

library(GGally)

library(DMwR)

library(plotly)

set.seed(5800)

prod<-read.csv("productcluster.csv")

head(prod)

str(prod)

summary(prod[,2:7])


prod.clean <- prod[prod$ITEM_SK != 11740941, ]


prod2<-prod.clean[,2:5]

head(prod2)

print(prod2)

prod.scale = scale(prod2)

data=prod.scale

source("betterkmeans.R")

# bkm <- function(data,k,iter)
# {
#   ans = kmeans(data,k,iter)
#   for(i in 1:10)
#   {
#     temp= kmeans(data,k,iter)
#     if(temp$tot.withinss < ans$tot.withinss)
#     {
#       ans = temp
#     }
#   }
#   ans
# }

lo=2
hi=50

size= hi-lo+1;

err= array(2*size, dim=c(size,2))

# i=lo
# 
# rowNum=i-lo+1
# err[rowNum,1]=i
# err[rowNum,2]=bkm(data,i,100)$tot.withinss


for(i in lo:hi)
{
  rowNum=i-lo+1
  err[rowNum,1]=i
  err[rowNum,2]=bkm(data,i,100)$tot.withinss
}
write.csv(err,file="errors.csv")
plot(err[,1],err[,2])

#is.matrix(err)
