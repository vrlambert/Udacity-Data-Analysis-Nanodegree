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

# Get all of the generation values for the past year
latest <- subset(energy, year == max(energy$year))

# Create a few plots exploring the data

ggplot(aes(x = generation), data = latest) + 
  geom_histogram() +
  scale_x_continuous(limits = c(0, 40000))

first <- subset(energy, year == min(energy$year))

ggplot(aes(x = generation), data = first) + 
  geom_histogram() +
  scale_x_continuous(limits = c(0, 40000))

ggplot(aes(x = year, y = generation, group = year), data = energy) +
  geom_boxplot()

