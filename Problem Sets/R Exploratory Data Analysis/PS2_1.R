# Problem Set 2
# Two variable analysis

library(ggplot2)
data("diamonds")

# Problem 1 create a scatterplot of price vs x.
ggplot(aes(x, price), data = diamonds) + 
  geom_point()

# Problem 2, observations about the problem 1 plot
# most of the data lies between x = 3 and x = 9,
# there are some points with missing x values
# the relationship seems exponential

# problem 3
cor.test(diamonds$price, diamonds$x)
cor.test(diamonds$price, diamonds$y)
cor.test(diamonds$price, diamonds$z)

# problem 4, plot depth vs price
ggplot(aes(depth, price), data = diamonds) + 
  geom_point()

# problem 5, adjust the transparency to 1/100 and the x axis to every 2
ggplot(aes(depth, price), data = diamonds) + 
  geom_point(alpha = 1/100) +
  scale_x_continuous(breaks = seq(0, 80, 2))

# Problem 6, what is the typical range for the depth of a particle
# 59 - 60

# problem 7
cor.test(diamonds$depth, diamonds$price)
# You wouldn't use this to predict the price of a diamond because the value is close to zero

# Problem 8
# Create a scatterplot of price vs carat
# and omit the top 1% of price and carat
# values.
ggplot(aes(price, carat), data = diamonds[diamonds$price < quantile(diamonds$price, 0.99) &
                                            diamonds$carat < quantile(diamonds$carat, 0.99),]) + 
  geom_point() 
  
# Problem 9
# create a new variable in diamonds called volume and plot it vs price
diamonds$volume <- with(diamonds, x*y*z)
ggplot(aes(volume, price), data = diamonds) +
  geom_point()

# Problem 10
# Observations from price vs volume scatter plot
# the plot is exponential, similar to size. There is one volume outlier near 3700 volume

# Problem 11
# calculate the correlation of price vs volume, not including volume 0 or greater than 800
d.vol_sub <- subset(diamonds, diamonds$volume != 0 &
                      diamonds$volume < 800)

with(d.vol_sub,
     cor.test(price, volume))

# Problem 12
# Improving the price/volume plot
ggplot(aes(volume, price), data = d.vol_sub) +
  geom_point(alpha = 1/20) + 
  geom_smooth(method = 'lm') + 
  ylim(0, 20000)

# Problem 13
# Use the function dplyr package
# to create a new data frame containing
# info on diamonds by clarity.

# Name the data frame diamondsByClarity

# The data frame should contain the following
# variables in this order.

#       (1) mean_price
#       (2) median_price
#       (3) min_price
#       (4) max_price
#       (5) n

# where n is the number of diamonds in each
# level of clarity.

diamondsByClarity <- diamonds %>%
  group_by(clarity) %>%
  summarise(mean_price = mean(price),
            median_price = median(price),
            min_price = min(price),
            max_price = max(price),
            n = n()) %>%
  arrange(clarity)
            
# Problem 14
# We’ve created summary data frames with the mean price
# by clarity and color. You can run the code in R to
# verify what data is in the variables diamonds_mp_by_clarity
# and diamonds_mp_by_color.

# Your task is to write additional code to create two bar plots
# on one output image using the grid.arrange() function from the package
# gridExtra.
diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

p1 <- ggplot(aes(clarity, mean_price), data = diamonds_mp_by_clarity) + 
  geom_col()

p2 <- ggplot(aes(color, mean_price), data = diamonds_mp_by_color) + 
  geom_col()

library(gridExtra)
grid.arrange(p1, p2) 





