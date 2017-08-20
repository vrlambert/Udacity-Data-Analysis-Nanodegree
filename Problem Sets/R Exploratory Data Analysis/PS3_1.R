data("diamonds")
diamonds$cut = factor(diamonds$cut,levels(diamonds$cut)[c(5, 4, 3, 2, 1)])

# Question 1
# Create a histogram of diamond prices.
# Facet the histogram by diamond color
# and use cut to color the histogram bars.
ggplot(aes(x = price), data = diamonds) +
  geom_histogram(aes(fill = cut)) +
  facet_wrap(~color) +
  scale_fill_brewer(type = 'qual') +
  scale_x_log10()

# Question 2
# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.
ggplot(aes(x = table, y = price), data = diamonds) +
  geom_point(aes(color = cut)) +
  scale_color_brewer(type = 'qual')

# Question 4
# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.
ggplot(aes(x = x * y * z, y = price),
       data = subset(diamonds, x * y * z < quantile(x * y * z, 0.99) &
                               x * y * z > 0)) +
  geom_point(aes(color = clarity)) + 
  scale_y_log10()

# Question 5
# Many interesting variables are derived from two or more others.
# For example, we might wonder how much of a person's network on
# a service like Facebook the user actively initiated. Two users
# with the same degree (or number of friends) might be very
# different if one initiated most of those connections on the
# service, while the other initiated very few. So it could be
# useful to consider this proportion of existing friendships that
# the user initiated. This might be a good predictor of how active
# a user is compared with their peers, or other traits, such as
# personality (i.e., is this person an extrovert?).

# Your task is to create a new variable called 'prop_initiated'
# in the Pseudo-Facebook data set. The variable should contain
# the proportion of friendships that the user initiated.
pf <- read.csv('pseudo_facebook.tsv', sep = '\t')
pf$prop_initiated <- pf$friendships_initiated / pf$friend_count
summary(pf$prop_initiated)

#Question 6
# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.
pf$year_joined <- floor(2014 - pf$tenure/365)
pf$year_joined.bucket <- cut(pf$year_joined, c(2004, 2009, 2011, 2012, 2014))
summary(pf$year_joined.bucket)

ggplot(aes(x = tenure, y = prop_initiated), 
       data = subset(pf, !is.na(pf$year_joined.bucket) &
                         !is.na(pf$prop_initiated))) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median)

# Question 7
# Smooth the last plot you created of
# of prop_initiated vs tenure colored by
# year_joined.bucket. You can bin together ranges
# of tenure or add a smoother to the plot.
ggplot(aes(x = tenure, y = prop_initiated), 
       data = subset(pf, !is.na(pf$year_joined.bucket) &
                       !is.na(pf$prop_initiated))) +
  geom_smooth(aes(color = year_joined.bucket))

# Question 9
# find the mean of the group with the highest prop_initated
by(pf$prop_initiated, pf$year_joined.bucket, mean, na.rm=TRUE)

# Question 10
# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.
ggplot(aes(x = cut, y = price/carat), data = diamonds) + 
  geom_jitter(aes(color = color)) +
  facet_wrap(~clarity) +
  scale_color_brewer(type = 'div')

