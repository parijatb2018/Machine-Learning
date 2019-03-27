bkm <- function(data,k,iter)
{
  ans = kmeans(data,k,iter)
  for(i in 1:10)
  {
    temp= kmeans(data,k,iter)
    if(temp$tot.withinss < ans$tot.withinss)
    {
      ans = temp
    }
  }
  ans
}