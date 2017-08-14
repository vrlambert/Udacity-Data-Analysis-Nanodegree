library(ggplot2)
data("diamonds")
# Question 1
nrow(diamonds)
ncol(diamonds)
?diamonds

# Question 2
qplot(x = price, data = diamonds)

# Question 3
mean(diamonds$price)
median(diamonds$price)
# It's a long tailed distribution

# Question 4
length(diamonds$price[diamonds$price < 500])
length(diamonds$price[diamonds$price < 250])
length(diamonds$price[diamonds$price > 15000])

# Question 5
# Explore the largest peak in the
# price histogram you created earlier.
ggplot(aes(x = price), data = diamonds) + 
  geom_histogram(binwidth = 40) + 
  scale_x_continuous(limits = c(0, 1500))

# Question 6
# Break out the histogram of diamond prices by cut.
ggplot(aes(x = price), data = diamonds) + 
  geom_histogram() + 
  facet_wrap(~cut)

# Question seven
# Prices by cut
by(diamonds$price, diamonds$cut, max)
by(diamonds$price, diamonds$cut, min)
by(diamonds$price, diamonds$cut, summary, digits = max(getOption('digits')))

# Question 8
# compare the shape with free y
ggplot(aes(x = price), data = diamonds) +
  geom_histogram(binwidth = 500) +
  facet_wrap(~cut, scales = 'free_y')

# Question 9
# plot the price per carat on a log scale
ggplot(aes(x = price/carat), data = diamonds) +
  geom_histogram(binwidth = 0.025) +
  scale_x_log10() +
  facet_wrap(~cut)

# Question 10
# create a box plot
ggplot(aes(x = color, y = price), data = diamonds) +
  geom_boxplot()

# Question 11 Interquartile Range
by(diamonds$price, diamonds$color, summary)
IQR(subset(diamonds, color == 'D')$price)
IQR(subset(diamonds, color == 'J')$price)

# Question 12
# box plots for color, price per carat
ggplot(aes(x = color, y = price/carat), data = diamonds) +
  geom_boxplot()

# Question 13
# Investigate the weight of diamonds using a frequency polygon
# Find values with count >2000
ggplot(aes(x = carat), data = diamonds) +
  geom_freqpoly(binwidth = 0.01) +
  scale_x_continuous(limits = c(0, 1.5))
