
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

withinSSrange <- function(data,low,high,maxIter)
{
  withinss = array(0, dim=c(high-low+1));
  
  print(" k    -       WCSS")
  print("---------------------")
  
  for(i in low:high)
  {
    withinss[i-low+1] <- kmeans(data, i, maxIter)$tot.withinss
 
   
    print (c(i,"-",round((withinss[i-low+1]),3)))
   
    
    }
 
  withinss
  
}




plot(withinSSrange(prod.scale,1,50,150), xlab="K Value"
     ,ylab="WCSS")


pkm = kmeans(prod.scale, 5, 150)



prod.realCenters = unscale(pkm$centers, prod.scale)


clusteredProd = cbind(prod.clean, pkm$cluster)

plot(clusteredProd[,2:5], col=pkm$cluster )


write.csv(clusteredProd, file = "results.csv",col.names = FALSE)

head(clusteredProd)

colnames(clusteredProd)<-c("itemid","totrev","baskets","noofcustomers",
                           "avgproductprice","productname","productcat","cluster") 

head(clusteredProd)
##---->> baskets vs revenue plot: to show clusters
ggplot(data=clusteredProd,aes(x=baskets,y= totrev, color= cluster))+
geom_point(size=2)+ ylab(" Total Revenue")+ggtitle("Baskets vs TotalRevenue")
                              
###<<<Bar graphs>>
  
##------->>> rev vs cluster

rev<-aggregate(totrev~cluster,clusteredProd,sum)

plot_ly(rev,x=~cluster,y=~totrev,type='bar')%>%
layout(xaxis = list(title = 'Cluster'),
       yaxis = list(title = 'Total Revenue'),barmode = 'group'
       ,title="Cluster vs Total Revenue")

##------->>> bas vs cluster

bas<-aggregate(baskets~cluster,clusteredProd,sum)

plot_ly(bas,x=~cluster,y=~baskets,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Baskets'),barmode = 'group'
         ,title="Cluster vs Baskets")

##------->>> cust vs cluster

cust<-aggregate(noofcustomers~cluster,clusteredProd,sum)

plot_ly(cust,x=~cluster,y=~noofcustomers,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'No of Customers'),barmode = 'group'
         ,title="Cluster vs No of Customer")

##------->>> avgprice vs cluster

avg1<-aggregate(avgproductprice~cluster,clusteredProd,mean)

plot_ly(avg1,x=~cluster,y=~avgproductprice,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'Average Product Price'),barmode = 'group'
         ,title="Cluster vs Average Product Price")

##----------->>> which cat giving highest rev
productcat11<-data.frame(totrev=clusteredProd$totrev,productcat=clusteredProd$productcat)

head(productcat1, n=7)

cat<-aggregate(totrev~productcat,productcat11,sum)


head(cat)

plot_ly(cat,x=~productcat,y=~totrev,type='bar')%>%
  layout(xaxis = list(title = 'Product Category'),
         yaxis = list(title = 'Total Revenue'),barmode = 'group',
         title="Product Category vs Total Revenue for All Clusters")


#   cat 5, 1, 3 ------------>>>
#cat 2>>>
productcat11<-data.frame(totrev=clusteredProd$totrev,productcat=clusteredProd$productcat,clusteredProd$cluster)


# Cat2 >>>>>
productcat11<-data.frame(totrev=clusteredProd$totrev,productcat=clusteredProd$productcat,clusteredProd$cluster)

productcat3<-productcat11[productcat11$cluster==2,]

head(productcat1, n=7)


cat<-aggregate(totrev~productcat,productcat3,sum)



head(cat)

plot_ly(cat,x=~productcat,y=~totrev,type='bar')%>%
  layout(xaxis = list(title = 'Product Category'),
         yaxis = list(title = 'Total Revenue'),barmode = 'group',
         title="Total Revenue vs Product Category for Cluster 2")


#cat 1

productcat11<-data.frame(totrev=clusteredProd$totrev,productcat=clusteredProd$productcat,clusteredProd$cluster)

productcat1<-productcat11[productcat11$cluster==1,]

head(productcat1, n=7)


cat<-aggregate(totrev~productcat,productcat1,sum)

#cat<-cat[order(-cat$totrev),]

#cat<- cat.reset_index()

head(cat)

plot_ly(cat,x=~productcat,y=~totrev,type='bar')%>%
  layout(xaxis = list(title = 'Product Category'),
         yaxis = list(title = 'Total Revenue'),barmode = 'group',
         title="Total Revenue vs Product Category for Cluster 1")



#>>> cat3

productcat11<-data.frame(totrev=clusteredProd$totrev,productcat=clusteredProd$productcat,clusteredProd$cluster)

productcat1<-productcat11[productcat11$cluster==3,]

head(productcat1, n=7)


cat<-aggregate(totrev~productcat,productcat1,sum)

#cat<-cat[order(-cat$totrev),]

#cat<- cat.reset_index()

head(cat)

plot_ly(cat,x=~productcat,y=~totrev,type='bar')%>%
  layout(xaxis = list(title = 'Product Category'),
         yaxis = list(title = 'Total Revenue'),barmode = 'group',
         title="Total Revenue vs Product Category for Cluster 3")



###----->>>> cluster vs product chart 

product12<-data.frame(products=clusteredProd$productname,cluster=clusteredProd$cluster)

#product50<-productcat12[productcat12$cluster==2,]

#product50

#summary(product50)
#str(product50)
#head(clusteredProd)
#head(product50, n=7)
library(dplyr)
x1<-count(product12,cluster)

#products10<-aggregate(products~cluster,product12,rowSums(table(unique(product12))))

#cat<-cat[order(-cat$totrev),]

#cat<- cat.reset_index()

#head(cat)

plot_ly(x1,x=~cluster,y=~n,type='bar')%>%
  layout(xaxis = list(title = 'Cluster'),
         yaxis = list(title = 'No of Products'),barmode = 'group',
         title="No of products vs cluster")

