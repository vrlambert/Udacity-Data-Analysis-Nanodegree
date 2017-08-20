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
