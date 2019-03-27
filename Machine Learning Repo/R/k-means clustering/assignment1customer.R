# Importing Libraries and read the input CSV
setwd("C:/Users/vivek/Documents/R Scripts/ass1")
library(ggplot2)
library(GGally)
library(DMwR)
library(plotly)
prod<-read.csv("customercluster.csv")


ggpairs(prod[, which(names(prod) != "CUSTOMER_SK")],
        upper = list(continuous = ggally_points),
        lower = list(continuous = "points"),
        title = "Products before outlier removal")

summary(prod[2:7])
prod.clean <- prod[prod$CUSTOMER_SK != 1, ]
prod.scale = scale(prod.clean[1:7])

##------->>> K Means Clustering

withinSSrange <- function(data,low,high,maxIter)
{
  withinss = array(0, dim=c(high-low+1));
  for(i in low:high)
  {
    withinss[i-low+1] <- kmeans(data, i, maxIter)$tot.withinss
  }
  withinss
}

plot(withinSSrange(prod.scale,1,50,150))

pkm = kmeans(prod.scale, 6, 150)

prod.realCenters = unscale(pkm$centers, prod.scale)

clusteredProd = cbind(prod.clean, pkm$cluster)

plot(clusteredProd[,2:7], col=pkm$cluster )

plot(clusteredProd[,4:6], col=pkm$cluster)

write.csv(clusteredProd, file = "resultsc.csv",col.names = FALSE)

head(clusteredProd)

colnames(clusteredProd)<-c("customer","quantity","totrev","recency","visits","products",
                           "avgspend","cluster") 
## ggplot

##------->>> Visits vs Average Spend

ggplot(data=clusteredProd,aes(x=visits,y= avgspend, color= cluster))+
geom_point(size=2)+ggtitle("Visits vs Average Spend")

u<-ggplot(data=clusteredProd,aes(x=visits,y= avgspend, color= cluster))
u+geom_point(size=2)+facet_grid(cluster~.)+ggtitle("Exploded Visits vs Average Spend")

##------->>> Visits vs Total Revenue

ggplot(data=clusteredProd,aes(x=visits,y= totrev,color= cluster))+
  geom_point(size=2)+ggtitle("Visits vs Total Revenue")

ggplot(data=clusteredProd,aes(x=visits,y= totrev,color= cluster))+
  geom_point(size=2)+facet_grid(cluster~.)+ggtitle("Exploded Visits vs Total Revenue")

u2<-ggplot(data = clusteredProd,aes(x=visits,y= totrev, color=cluster))
  u2+geom_boxplot(size=1.2)+facet_grid(cluster~.)

u3<-clusteredProd[clusteredProd$totrev]

u5<-ggplot(data=clusteredProd,aes(x= totrev,y=cluster))
u5+geom_bar()

## bar chart

##------->>> rev vs cluster

rev<-aggregate(totrev~cluster,clusteredProd,sum)

plot_ly(rev,x=~cluster,y=~totrev,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Total Spend'),barmode = 'group'
         ,title="Cluster vs Total Spend")

##------->>> avgprice vs cluster

rev1<-aggregate(avgspend~cluster,clusteredProd,mean)

plot_ly(rev1,x=~cluster,y=~avgspend,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Avg spend'),barmode = 'group'
         ,title="Cluster vs Mean Average Spend")

##------->>> recency vs cluster

rev2<-aggregate(recency~cluster,clusteredProd,mean)

plot_ly(rev2,x=~cluster,y=~recency,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Recency'),barmode = 'group'
         ,title="Cluster vs Mean Recency")

##------->>> Visits vs cluster

rev3<-aggregate(visits~cluster,clusteredProd,sum)

plot_ly(rev3,x=~cluster,y=~visits,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Visits'),barmode = 'group'
         ,title="Cluster vs Total Visits")

##------->>> products vs cluster

rev3<-aggregate(products~cluster,clusteredProd,sum)

plot_ly(rev3,x=~cluster,y=~products,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'products'),barmode = 'group'
         ,title="Cluster vs Total quantity")

##------->> Plotting the population of clusters

product12<-data.frame(customer=clusteredProd$customer,cluster=clusteredProd$cluster)
aggregate

products10<-aggregate(customer~cluster,product12,count)
library(dplyr)

# calculation of the count of customer under a cluster
p<-count(product12,cluster)

plot_ly(p,x=~cluster,y=~n,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'No of Customers'),barmode = 'group',
         title="No of customers vs cluster")




