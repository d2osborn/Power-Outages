# Power Outages Energy Consumption Statistical Analysis
Power outage energy consumption statistical analysis is an extensive data science project for DSC 80 at UC San Diego. It involves several stages of statistical analysis, from data cleaning and exploratory data analysis to assessing missingness, hypothesis testing, framing a prediction problem (its baseline and final model), and a fairness analysis. This project aims to deduce the most influential characteristics of a major power outage, and how it can help energy companies lead to more efficient allocation of resources, reduced economic losses, and increased safety for individuals and infrastructure.

Author: Diego Osborn

## Introduction
One major issue that's constantly being faced globally is the occurrence of power outages. Power outages pose a problem because they can disrupt daily life, impact critical services, pose safety risks, and result in economic losses for individuals, businesses, and communities. The dataset I will be working on is the data that was used in an article by Sayanti Mukherjee et al., "A Multi-Hazard Approach to Assess Severe Weather-Induced Major Power Outage Risks in the U.S.", and can be accessed from Purdue University’s Laboratory for Advancing Sustainable Critical Infrastructure, at https://engineering.purdue.edu/LASCI/research-data/outages.

This dataset covers **major power outages**--outages that affected at least 50,000 customers or caused an unplanned firm load loss of at least 300 MW--in the U.S. from January 2000 to July 2016, which includes several important features such as geographical location, timing, climatic conditions, land-use characteristics, electricity consumption, and economic attributes of the affected states.

The central question I am interested in is: **What are the characteristics of major power outages with higher severity?** I want to use data analysis to understand which characteristics have the highest impact on major power outages, and using this knowledge I can set up a model that predicts the energy consumption of an area. Accurately predicting the energy consumption levels of an area allows energy companies to effectively manage and allocate resources, ensuring a stable and reliable supply of electricity. Leading to more reliable electricity services, reduced economic losses, and increased safety for individuals and infrastructure.

The dataset, outage, contains 1534 rows, each being a unique record of a major power outage, with 56 columns. Here's a brief description of some of the columns that are relevant to my analysis:

- `YEAR`: Indicates the year when the outage event occurred

- `U.S._STATE`: Represents all the states in the continental U.S.

- `POSTAL.CODE`: Represents the postal code of the U.S. states

- `NERC.REGION`: The North American Electric Reliability Corporation (NERC) regions involved in the outage event

- `CLIMATE.REGION`: U.S. Climate regions as specified by National Centers for Environmental Information (nine climatically consistent regions in continental U.S.A.)

- `OUTAGE.START`: This variable indicates the day of the year and the time of the day when the outage event started (as reported by the corresponding Utility in the region)

- `OUTAGE.RESTORATION`: This variable indicates the day of the year and the time of the day when power was restored to all the customers (as reported by the corresponding Utility in the region)

- `OUTAGE.DURATION`: Duration of outage events (in minutes)

- `DEMAND.LOSS.MW`: Amount of peak demand lost during an outage event (in Megawatt) [but in many cases, total demand is reported]

- `CUSTOMERS.AFFECTED`: Number of customers affected by the power outage event

- `RES.SALES`: 	Electricity consumption in the residential sector (megawatt-hour)

- `COM.SALES`: 	Electricity consumption in the commercial sector (megawatt-hour)

- `IND.SALES`: Electricity consumption in the industrial sector (megawatt-hour)

- `TOTAL.SALES`: Total electricity consumption in the U.S. state (megawatt-hour)

- `PC.REALGSP.STATE`: Per capita real gross state product (GSP) in the U.S. state (measured in 2009 chained U.S. dollars)

- `POPULATION`: Population in the U.S. state in a year

- `PCT_WATER_TOT`: Percentage of water area in the U.S. state as compared to the overall water area in the continental U.S. (in %)

# Step 2: Data Cleaning and Exploratory Data Analysis
## Data Cleaning

When loading the outage dataframe from an Excel file, I encountered two main issues. First, the file included a brief overview spanning four rows and the first column, which I removed to focus on the actual data and columns. Second, the column names were initially 'Unnamed: #', with the actual column names located below the first four rows. To fix this, I sliced the dataframe and reassigned the column names to the values in the first row. This left me with a dataframe that was ready to be explored.

The next step I took was combining the columns `OUTAGE.START.DATE` and `OUTAGE.START.TIME` into one `OUTAGE.START` timestamp column, and the same for `OUTAGE.RESTORATION`. I did this to reduce the number of columns and make the date and time information easier to manage as a single entity. As a result I dropped the original `DATE` and `TIME` columns for both `START` and `RESTORATION`.

Then, I changed the data types of each column to ensure that each column has its correct respective null type and data type. This allows me to perform manipulations on the columns without encountering errors due to incorrect types.

Below is the head of the cleaned `power_outage` dataframe with relevant columns.

<div style="text-align: center;">

|   YEAR | POSTAL.CODE   | NERC.REGION   | CLIMATE.REGION     | OUTAGE.START        | OUTAGE.RESTORATION   |   OUTAGE.DURATION | DEMAND.LOSS.MW   | CUSTOMERS.AFFECTED   |   RES.SALES |   COM.SALES |   IND.SALES |   TOTAL.SALES |   PCT_WATER_TOT |
|-------:|:--------------|:--------------|:-------------------|:--------------------|:---------------------|------------------:|:-----------------|:---------------------|------------:|------------:|------------:|--------------:|----------------:|
|   2011 | MN            | MRO           | East North Central | 2011-07-01 17:00:00 | 2011-07-03 20:00:00  |              3060 | <NA>             | 70000                |     2332915 |     2114774 |     2113291 |       6562520 |         8.40733 |
|   2014 | MN            | MRO           | East North Central | 2014-05-11 18:38:00 | 2014-05-11 18:39:00  |                 1 | <NA>             | <NA>                 |     1586986 |     1807756 |     1887927 |       5284231 |         8.40733 |
|   2010 | MN            | MRO           | East North Central | 2010-10-26 20:00:00 | 2010-10-28 22:00:00  |              3000 | <NA>             | 70000                |     1467293 |     1801683 |     1951295 |       5222116 |         8.40733 |
|   2012 | MN            | MRO           | East North Central | 2012-06-19 04:30:00 | 2012-06-20 23:00:00  |              2550 | <NA>             | 68200                |     1851519 |     1941174 |     1993026 |       5787064 |         8.40733 |
|   2015 | MN            | MRO           | East North Central | 2015-07-18 02:00:00 | 2015-07-19 07:00:00  |              1740 | 250              | 250000               |     2028875 |     2161612 |     1777937 |       5970339 |         8.40733 |

</div>

<iframe
  src="assets/total-sales-per-year.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>