library(readxl)
library(tidyr)
library(ggplot2)

# First import the excel file
energy_data_raw <- read_excel('Electricity Generation per capita.xlsx')

# Now gather the raw data into a new, tidy dataframe
energy <- gather(energy_data_raw, 
                key = 'year', 
                value = 'generation',
                colnames(energy_data_raw)[-1],
                convert = TRUE)

# change the name of the first column to something more reasonable
colnames(energy)[1] <- 'country'

# Check out a summary to make sure everything looks ok
summary(energy)

e.desired = subset(energy, country == 'United States' |
                           country == 'China' |
                           country == 'India')

ggplot(aes(year, generation), data = energy) + 
  geom_point()

# Line plot of energy use over time for china, india, and usa
ggplot(aes(x = year, 
           y = generation, 
           color = country, 
           group = country), 
       data = e.desired) +
  geom_line()

energy.wide <- spread(energy, country, generation)

ggplot(aes(year, generation), data = subset(energy, generation > 10000)) + 
  geom_line(aes(color = country))
