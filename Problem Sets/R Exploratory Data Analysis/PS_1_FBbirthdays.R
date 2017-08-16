library(lubridate)
library(readr)
library(ggplot2)
birthdays_raw <- read_csv('FB friends birthdays.csv',
                          col_types =  cols(
                            Friend = col_integer(),
                            `Start date` = col_date(format = "%m/%d/%y"),
                            `End date` = col_character(),
                            `Start time` = col_character(),
                            `End time` = col_character(),
                            Duration = col_character()
                          ));

birthdays  <-  birthdays_raw[c(1,2)]

ggplot(data = birthdays, aes(x = month(birthdays$`Start date`))) + 
  geom_histogram(bins = 12)

