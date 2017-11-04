# Summary
Effective Yield is a measure of the profit of a Prosper loan, and in this visualization we investigate the relationship between risk and yield. We start with an introduction to the demographics of Prosper loans. Next, we investigate the relationship between Prosper score, loan size, and yield. Finally, we investigate what drives Prosper score.

# Design

In this section I detail my findings during exploration, how I initially thought to visualize these findings, and how my visualizations changed with some feedback.

### Exploration

When looking at the variables available, my initial thoughts focused on two questions:

1. What are the most profitable loans?
1. What makes these loans more profitable?

I used the data field EstimatedEffectiveYield to compare the profitability of loans, and identified several variables that correlate strongly with the yield.

For the first question, I found that Prosper score provided a convenient and large impact on the profitability of the loan. In addition, loan size was a large factor.

For the second question, I looked into what factors influence the prosper score. I found that credit score and income were large drivers of the prosper score.

### Initial Design

Link: https://public.tableau.com/profile/victor.lambert#!/vizhome/ProsperLoanData_6/ProsperStory

I knew I wanted to have three dashboards from the start - one for a brief introduction to Proser loans and to the Prosper score, another diving deeper into the relationship between Prosper score and yield, and a final page showing the factors that impact Prosper score.

For the first dashboard, I wanted to show a few things:

- The geographic distribution of the loans
- The normal size of the loans
- The basic relationship between prosper score, APR, and yield

I settled on using a map to display the number of loans in each state, a bar chart of the frequency of loans of different sizes, and a line chart to show the relationship between Prosper score, yield, and APR. I thought that this dashboard was a good introduction to the Prosper loans.

To dive deeper into the Prosper score and yield, I made two more plots. One showing the distribution of Prosper scores, so people had a better idea of how many loans get each score. For the first iteration I used a histogram with bins of width 1.

The other plot shows yield vs loan size colored by Prosper score. I first started with a line graph of loan size vs yield, which was far too noisy. I used a moving average to better show the trend. After splitting the line into different colors for Prosper score, the second plot highlights one very interesting finding - that small, risky loans do not have nearly as good a yield as other loans. It also demonstrates that loans of Prosper score 4-5 actually make the most money.

For the second dashboard I used a continuous color scheme because the Prosper score is a scale of similar meaning.

Lastly, I wanted to display the factors that influence Prosper score. I used another line plot to show the relationship between credit score and Prosper score, which was very strong. I also wanted to show another variable which affected the score, Income. So I added a pie chart showing the distribution of income range, and used it to split the credit score plot based on income. I think the third dashboard provides good insight on what drives the Prosper score.

### Feedback Edits
Link: https://public.tableau.com/profile/victor.lambert#!/vizhome/ProsperLoanDataafterfeedback/ProsperStory

There were a few key takeaways from the feedback. My reviewers got the basic ideas of the visualizations, however the understanding wasn't perfect. I used their feedback to edit the text portion of my visualizations to make it more clear.

For the second dashboard, I had to edit the distribution figure. Rather than use histogram bins, which led to a confusing range of Prosper score, I switched to a bar chart. The advantage of the bar chart was it only listed the real values of Prosper score.

On the third dashboard, I removed the $0 income range because there were not many data points. This caused confusion over whether it was even in the pie chart.

# Feedback
Below you will see all the feedback I received, anonymously.
### Feedback #1:

I like it!

Sometimes there is Prosper Score, sometimes Prosper score, and sometimes prosper score.  Different capitalizations throughout.

It took me two reads before I realized the graphics changed when I put my mouse arrow over them, which I guess is OK. Once I saw that it got way cooler.
I don’t know what (bin) means where it is indicated.
On the last graph, the dark blue line is not in the pie chart above it, which seems odd.

Have a bit of trouble understanding the second page.  “pattery”?  Count of Prosper Score, is the number of scores?

The first page made me think a high Prosper score resulted in low yields for the lender.  The last page made me think a high prosper score is less risky.

I never heard of Prosper Score before, now I have a clue…. Is it a real thing?

### Feedback #2:
Peer-to-peer lending:  is this individuals lending to other individuals?  So the Prosper company connects people with money to lend to people that need a loan?  For instance, if mom and dad had an extra $5000, we could let Prosper know and they would lend the money for us and we would make a little money? I'm not sure your graphics need to address this but I am curious.

What is the numeric range of the Prosper Score - is it 0-10 with 10 being the best?  The bar graph on the second tab shows that the Prosper Score goes to 12?

As Dad noted, "pattern" is spelled incorrectly on the second tab

The final results are pretty clear - borrowers that have money and a decent credit score are a good risk for a Prosper loan.

# Resources
N/A
