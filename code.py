# --------------
# Load Data and Compute total
# The first step - you know the drill by now - load the dataset and see how it looks like. Additionally, calculate the total amount in the first quarter of the financial year. Calculate the total amount of all the users for the month of jan, feb and Mar and also grand total.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Code starts here

# Load dataset using pandas read_csv api in variable df and give file path as path.

df = pd.read_csv(path)

df.head()


# Convert the names of the states in state columns to lowercase and store it back in the same column


df["state"] = df["state"].apply(lambda s:s.lower())


# Create a new column named total which computes the total amount in the first quarter of the financial year i.e. for the months of Jan, Feb and Mar and store it in df['total']

df["total"] = df["Jan"]+df["Feb"]+df["Mar"]



# Calculate the sum of amount of all users in the Month of Jan, Feb, March and store it in variable sum_row (Here the sum implies the sum of all the entries in the Jan Column, sum of entries in Feb Column and Grand total stands for the sum of entries in the column total)


sum_row = df[["Jan","Feb","Mar","total"]].sum()


total_df = pd.DataFrame(data=sum_row).T


# Append this computed sum to the DataFrame df_final



df_final = df.append(total_df,ignore_index=True)


# Code ends here


# --------------
# Scrape Data From the web
# Here, you will be scraping data from the web and cleaning it.


import requests


# Code starts here


# Scrapes the url https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations and store it in variable url

url = "https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations"



# Use module requests to get the url and store it in variable called response


response = requests.get(url)


# load the html file in dataframe df1. Note:use pd.read_html(response.content)[0].

df1 = pd.read_html(response.content)[0]



# First few rows consists of unclean data. You need to select rows from index 11 till end. Make the values at index 11 as column headers and store it in dataframe df1

headers = df1.iloc[11]

df1 = pd.DataFrame(df1.values[12:],columns=headers)


# Remove space from the column named 'United States of America' and store the result in dataframe called df1['United States of America']


df1['United States of America'] = df1['United States of America'].apply(lambda s: s.strip())





# Code ends here


# --------------
# Mapping Countries to their abbreviations
# Using the data scraped from the previous task map abbreviation to the name of states.


df1["United States of America"] = df1["United States of America"].astype(str).apply(lambda x: x.lower())
df1["US"] = df1["US"].astype(str)

# Code starts here


# Using the scraped data which is stored in dataframe df1 create a variable called mapping which has the Country as key and Abbreviation as value



mapping = dict(df1.set_index("United States of America")["US"])

print(mapping)



# Create a new column called abbr as the 7th column (index = 6) of the DataFrame df_final
# map the df_final['state'] on variable mapping and store it in df_final['abbr']


df_final["abbr"] = df_final["state"].map(mapping)



# Code ends here


# --------------
# Filling in the Missing Values
# What you will notice in the previous task is that for two states Mississippi and Tennessee will have NaN values in column abbr. In this task you will be filling those missing values manually.


# Code stars here

# For the row where state=mississipi, replace the nan value of abbr column with MS

# For the row where state=tenessee, replace the nan value of abbr column with TN

df_final["abbr"] = np.where(df_final["state"]=="mississipi" , "MS" , np.where(df_final["state"]=="tenessee","TN","MS"))




# For the row where state=mississipi, replace the nan value of abbr column with MS


# df_final["abbr"] = df_final["abbr"][df_final.state=="mississipi"] ="MS"


# For the row where state=tenessee, replace the nan value of abbr column with TN


# df_final["abbr"] = df_final["abbr"][df_final.state=="tenessee"] ="TN"




# Code ends here


# --------------
# Total amount bank hold
# Here, use the newly created abbr column to understand the total amount that the bank holds in each state. Let us make this data frame more readable by introducing units in this case $ sign representing the unit of none




# Code starts here


# Groups by abbr and finds the sum of abbr,Jan,Feb ,Mar and total store the result in df_sub(use .groupby.() method)

df_sub=df_final[["abbr", "Jan", "Feb", "Mar", "total"]].groupby("abbr").sum()

print(df_sub)

print(df_sub.shape)

# Write a lambda function to introduce $ sign infront of all the numbers using applymap and store the result in formatted_df


formatted_df = df_sub.applymap(lambda x: "${:,.0f}".format(x))

formatted_df

# Code ends here




# --------------
# Append a row to the DataFrame
# In this task, you will append a row to the data frame which will give us information about the total amount of the various regions in Jan, Feb and march and also the grand total


# Code starts here

# Compute and store the sum of values of month of Jan, Feb, March and the Grand Total separately in a dataframe called 'sum_row' (Here the sum implies the sum of all the entries in the columns "Jan", "Feb", "Mar" and "total" respectively) [Hint: Use df.sum()]


sum_row = df_sub[["Jan", "Feb", "Mar", "total"]].sum()


# Tranpose the dataframe 'sum_row' and store it in a new dataframe 'df_sub_sum'


df_sub_sum = pd.DataFrame(data=sum_row).T


# Add $ in the beginning of all the entries of 'df_sub_sum' and store it back into the same dataframe.



df_sub_sum = df_sub_sum.applymap(lambda x: "${:,.0f}".format(x))


# Append 'df_sub_sum' to the 'formatted_df' dataframe and store the new resulting dataframe in 'final_table'

final_table = formatted_df.append(df_sub_sum)


# Print 'final_table'

print(final_table)


# The last row of final_table will have index =0. Rename that index to Total

final_table = final_table.rename(index={0: "Total"})





# Code ends here


# --------------
# Pie chart for total

# Having prepared all the data now its time to present the results visually.

# Code starts here


# add the total of all the three months and store it in variable called df_sub['total']

df_sub["total"] = df_sub["Jan"] + df_sub["Feb"] + df_sub["Mar"]


print(df_sub["total"])



# plot the pie chart for the df_sub['total']

df_sub["total"].plot(kind="pie" , subplots=True, figsize=(8,8))

plt.title("PIE CHART FOR TOTAL")

plt.legend(df_sub["total"])





# Code ends here


