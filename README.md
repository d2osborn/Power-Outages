# Power Outages Energy Consumption Statistical Analysis
Power outage energy consumption statistical analysis is an extensive data science project for DSC 80 at UC San Diego. It involves several stages of statistical analysis, from data cleaning and exploratory data analysis to assessing missingness, hypothesis testing, framing a prediction problem (its baseline and final model), and a fairness analysis. This project aims to deduce the most influential characteristics of a major power outage, and how it can help energy companies lead to more efficient allocation of resources, reduced economic losses, and increased safety for individuals and infrastructure.

Author: Diego Osborn

## Introduction
One major issue that's constantly being faced globally is the occurrence of power outages. Power outages pose a problem because they can disrupt daily life, impact critical services, pose safety risks, and result in economic losses for individuals, businesses, and communities. The dataset I will be working on is the data that was used in an article by Sayanti Mukherjee et al., "A Multi-Hazard Approach to Assess Severe Weather-Induced Major Power Outage Risks in the U.S.", and can be accessed from Purdue University’s Laboratory for Advancing Sustainable Critical Infrastructure, at https://engineering.purdue.edu/LASCI/research-data/outages.

This dataset covers **major power outages**--outages that affected at least 50,000 customers or caused an unplanned firm load loss of at least 300 MW--in the U.S. from January 2000 to July 2016, which includes several important features such as geographical location, timing, climatic conditions, land-use characteristics, electricity consumption, and economic attributes of the affected states.

The central question I am interested in is: **What are the characteristics of major power outages with higher severity?** I want to use data analysis to understand which characteristics have the highest impact on major power outages, and using this knowledge I can set up a model that predicts the energy consumption of an area. Accurately predicting the energy consumption levels of an area allows energy companies to effectively manage and allocate resources, ensuring a stable and reliable supply of electricity. Leading to more reliable electricity services, reduced economic losses, and increased safety for individuals and infrastructure.

The dataset, outage, contains 1534 rows, each being a unique record of a major power outage, with 56 columns. Here's a brief description of some of the columns that are relevant to my analysis:

| Column | Description |
|--------|-------------|
| `YEAR` | Indicates the year when the outage event occurred |
| `MONTH` | Indicates the month when the outage event occurred |
| `U.S._STATE` | Represents all the states in the continental U.S. |
| `POSTAL.CODE` | Represents the postal code of the U.S. states |
| `NERC.REGION` | The North American Electric Reliability Corporation (NERC) regions involved in the outage event |
| `CLIMATE.REGION` | U.S. Climate regions as specified by National Centers for Environmental Information (nine climatically consistent regions in continental U.S.A.) |
| `OUTAGE.START.DATE` | This variable indicates the day of the year when the outage event started (as reported by the corresponding Utility in the region) |
| `OUTAGE.START.TIME` | This variable indicates the time of the day when the outage event started (as reported by the corresponding Utility in the region) |
| `OUTAGE.RESTORATION.DATE` | This variable indicates the day of the year when power was restored to all the customers (as reported by the corresponding Utility in the region) |
| `OUTAGE.RESTORATION.TIME` | This variable indicates the time of the day when power was restored to all the customers (as reported by the corresponding Utility in the region) |
| `OUTAGE.DURATION` | Duration of outage events (in minutes) |
| `DEMAND.LOSS.MW` | Amount of peak demand lost during an outage event (in Megawatt) [but in many cases, total demand is reported] |
| `CUSTOMERS.AFFECTED` | Number of customers affected by the power outage event |
| `TOTAL.SALES` | Total electricity consumption in the U.S. state (megawatt-hour) |
| `PC.REALGSP.STATE` | Per capita real gross state product (GSP) in the U.S. state (measured in 2009 chained U.S. dollars) |
| `POPULATION` | Population in the U.S. state in a year |

# Step 2: Data Cleaning and Exploratory Data Analysis
## Data Cleaning

When loading the outage dataframe from an Excel file, I encountered two main issues. First, the file included a brief overview spanning four rows and the first column, which I removed to focus on the actual data and columns. Second, the column names were initially 'Unnamed: #', with the actual column names located below the first four rows. To fix this, I sliced the dataframe and reassigned the column names to the values in the first row. This left me with a dataframe that was ready to be explored.

The next step I took was combining the columns `OUTAGE.START.DATE` and `OUTAGE.START.TIME` into one `OUTAGE.START` timestamp column, and the same for `OUTAGE.RESTORATION`. I did this to reduce the number of columns and make the date and time information easier to manage as a single entity. As a result I dropped the original `DATE` and `TIME` columns for both `START` and `RESTORATION`.

I then replaced every 0 value in the columns `OUTAGE.DURATION`, `DEMAND.LOSS.MW`, and `CUSTOMERS.AFFECTED` as having a value of 0 for any of these columns are not characteristics of a major power outage. Inferring that 0 values are placeholders for missing values.

I then changed the data types of each column to ensure that each column has its correct respective data type. This allows me to perform manipulations on the columns without encountering errors due to incorrect types. To prevent errors from inconsistent null types after changing the data types of the columns, I replaced all null values with NumPy's NaN for consistency.

I also added a new column `IS_DARK`, which represents whether or not the outage occured during the daytime or nighttime. This column allows me to categorize outages to understand patterns such as when outages are more likely to occur.

Below is the head of the cleaned `power_outage` dataframe with relevant columns.
  
|   YEAR |   MONTH | OUTAGE.START        | OUTAGE.RESTORATION   | IS_DARK   | U.S._STATE   | CLIMATE.REGION     |   OUTAGE.DURATION |   DEMAND.LOSS.MW |   CUSTOMERS.AFFECTED |   TOTAL.SALES |   POPULATION |
|-------:|--------:|:--------------------|:---------------------|:----------|:-------------|:-------------------|------------------:|-----------------:|---------------------:|--------------:|-------------:|
|   2011 |       7 | 2011-07-01 17:00:00 | 2011-07-03 20:00:00  | False     | Minnesota    | East North Central |              3060 |              nan |                70000 |   6.56252e+06 |      5348119 |
|   2014 |       5 | 2014-05-11 18:38:00 | 2014-05-11 18:39:00  | False     | Minnesota    | East North Central |                 1 |              nan |                  nan |   5.28423e+06 |      5457125 |
|   2010 |      10 | 2010-10-26 20:00:00 | 2010-10-28 22:00:00  | True      | Minnesota    | East North Central |              3000 |              nan |                70000 |   5.22212e+06 |      5310903 |
|   2012 |       6 | 2012-06-19 04:30:00 | 2012-06-20 23:00:00  | True      | Minnesota    | East North Central |              2550 |              nan |                68200 |   5.78706e+06 |      5380443 |
|   2015 |       7 | 2015-07-18 02:00:00 | 2015-07-19 07:00:00  | True      | Minnesota    | East North Central |              1740 |              250 |               250000 |   5.97034e+06 |      5489594 |

# Exploratory Data Analysis
## Univariate Analysis

The bar plot below shows the distribution of power outages during the day and night times. This distribution helps us understand whether outages are more likely to occur during certain times of the day.
<iframe
  src="assets/outages-during-day-and-night.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>
From the plot, we can see that the majority of power outages occur during the day, with 1124 incidents, compared to 410 incidents at night. This indicates that major power outages are more prevalent during daytime hours. This could be due to higher electricity consumption and greater strain on the power grid during the day when businesses and households are active.

<iframe
  src="assets/total-sales-per-year.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>
<iframe
  src="assets/average-energy-consumption-per-state.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

## Bivariate Analysis

## Interesting Aggregates