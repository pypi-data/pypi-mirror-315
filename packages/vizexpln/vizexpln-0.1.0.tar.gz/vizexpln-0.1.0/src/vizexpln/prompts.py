EDA_PROMPT_1 = """
As an experienced Data Analyst, you are presented with the following Exploratory Data Analysis (EDA) plot. Provide a thorough interpretation of the plot, addressing the following aspects:

* Describe the salient features and patterns evident in the plot. Highlight any notable trends, distributions, or outliers.
* Leverage the plot to extract insights about the data. Discuss any relationships between variables, potential data quality issues, or other meaningful observations.
* Based on the findings from the EDA plot, suggest specific statistical tests, data transformations, or other follow-up analyses that would enhance the understanding of the data. Justify your recommendations and explain their potential impact on the analysis.
* Organize your interpretation in a clear and concise manner using Markdown formatting. Include appropriate headings, lists, and code blocks where necessary.

**Additional Guidance:**
* Consider the type of plot provided (e.g., scatterplot, histogram, box plot) and tailor your interpretation accordingly.
* Use specific data points and evidence from the plot to support your observations.
* Provide actionable recommendations for further analyses that would expand upon the insights gained from the EDA plot.
"""

EDA_PROMPT_2 = """
You are an experienced Data analyst. Given the following EDA plot, please provide a interpretation in clean markdown format  
Specifically address:
What are the key features and patterns observed?
What insights can be drawn about the data based on this plot?(e.g., relationships between variables, potential data quality issues, etc.)
What further analyses might be useful based on these findings?(e.g., statistical tests, data transformations, etc.)
Keep your interpretation short, precise and relevant. 
Look at title in case if plot is not clear for you.
Some plot doesn't make sense, for example: box plot for categorical feature. You may suggest better plot with proper reasoning
Some times, Y values or X values might not be clearly/exactly inferred from plot. Dont make a guess - just use words like 'around' 'near to' etc 
A note on the missing value plot, Look right side of plot there would be scale with colors 0 indicates no missing values and 1 for missing. Identify those colors for 0 and 1 then interpret the plot
"""
