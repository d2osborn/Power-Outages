# Power Outages Statistical Analysis
Energy demand forecaster: predicting regional energy consumption is an extensive data science project for DSC 80 at UC San Diego. It involves several stages of statistical analysis, from data cleaning and exploratory data analysis to assessing missingness, hypothesis testing, framing a prediction problem (its baseline and final model), and a fairness analysis. This project aims to deduce the most influential characteristics of a major power outage, and how it can help energy companies lead to more efficient allocation of resources, reduced economic losses, and increased safety for individuals and infrastructure.

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

I added a new column `IS_DARK`, which represents whether or not the outage occured during the daytime (6 AM to 8 PM) or nighttime (8 PM to 6 AM). This column allows me to categorize outages to understand patterns such as when outages are more likely to occur. This column also accounts for NaN values from `OUTAGE.START` by also being null.

I dropped the columns `CAUSE.CATEGORY.DETAIL` and `HURRICANE.NAMES` because I deemed them irrelevant as they are categorical variables whose values hold no weight in my analysis.

I also filtered the dataset to exclude rows from Alaska and Hawaii because the dataset is meant to represent data from the continental USA. Additionally, there were too many missing values in the record of the outage event for these rows, so it was better to exclude them completely.

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
  frameborder="0"></iframe> 
From the plot, we can see that the majority of power outages occur during the day, with 1124 incidents, compared to 410 incidents at night. This indicates that major power outages are more prevalent during daytime hours. This could be due to higher electricity consumption and greater strain on the power grid during the day when businesses and households are active.

The histogram below illustrates the distribution of total electricity sales recorded in the dataset.
<iframe
  src="assets/distrib-of-total-sales.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
The histogram shows that total electricity sales are right-skewed, indicating that most records reflect lower to moderate sales, while a few exhibit significantly higher sales. This suggests that occasional high consumption could correlate with major power outages, as increased demand strains the power grid. Understanding this distribution helps identify patterns that may influence outage severity and frequency.

## Bivariate Analysis

The bar plot below shows the median outage duration for each month:
<iframe
  src="assets/median-outage-per-month.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
The plot reveals that power outages are more severe in the Winter due to winter storms and accessibility issues (the storms make it difficult for repair crews to access damaged areas), but also particularly the highest in August and September. This could be attributed to extreme weather events such as hurricanes and heatwaves, which are common during these months and can cause significant damage to the power grid, and accumulated wear and tear on the grid and resources from earlier summer events might lead to longer outages. In contrast, the lowest median outage duration is during the Spring and Summer, suggesting that outages are dealt with faster due to better weather conditions and fewer severe weather disruptions.

The bar plot below shows the count of power outage events for each month:
<iframe
  src="assets/outages-per-month.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
The plot reveals that power outages are more frequent in the summer months, particularly in June and July, which may be due to increased electricity demand from air conditioning and summer storms. In contrast, the lowest number of outages occurs during Spring and Fall, suggesting lower overall demand and fewer severe weather events during this time.

The choropleth map below displays the median outage duration per state based on the dataset provided.
<iframe
  src="assets/median-duration-per-state.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
From the map, we observe significant variations in median outage duration across different states. States such as Michigan (MI), New York (NY), and West Virginia (WV) exhibit longer median outage durations, represented by darker shades, indicating that these states experience more prolonged outages on average. This visualization highlights the disparities in power outage experiences across the United States, suggesting areas where infrastructure improvements may be most needed to reduce the impact of power outages.

The scatter plot below displays the relationship between `TOTAL.SALES` and `CUSTOMERS.AFFECTED`.
<iframe
  src="assets/sales-vs-customers.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
The plot reveals that there is a weak positive relationship between Total Sales and Customers Affected, suggesting that while there is a slight tendency for more customers to be affected by power outages as total sales increase, the relationship is not strong. Other factors likely play a more significant role in determining the number of customers affected by outages, and total sales alone are not a reliable predictor.

## Interesting Aggregates

The grouped table by `NERC.REGION`, displaying the median `OUTAGE.DURATION`, `DEMAND.LOSS.MW`, and `CUSTOMERS.AFFECTED` below, highlights significant regional differences in the severity of power outages. Regions like ECAR and HI experience the longest median outage durations and highest median demand losses, indicating greater vulnerability and more severe impacts during outages, which can guide energy companies and policymakers in prioritizing infrastructure improvements and emergency response efforts to mitigate these severe outages.

| NERC.REGION   |   OUTAGE.DURATION |   DEMAND.LOSS.MW |   CUSTOMERS.AFFECTED |
|:--------------|------------------:|-----------------:|---------------------:|
| ASCC          |               nan |               35 |                14273 |
| ECAR          |             5475  |              350 |               142500 |
| FRCC          |             1419  |              265 |                94475 |
| FRCC, SERC    |              372  |              nan |                  nan |
| HECO          |              543  |              120 |                59886 |
| HI            |             1367  |             1060 |               294000 |
| MRO           |             1272  |              373 |                69100 |
| NPCC          |             993.5 |              225 |                70500 |
| PR            |              174  |              220 |                62000 |
| RFC           |            2002.5 |              285 |               121000 |
| SERC          |              803  |            291.5 |                75000 |
| SPP           |             1273  |              200 |                70000 |
| TRE           |             1110  |              350 |               113247 |
| WECC          |             248.5 |              220 |                84500 |

The pivot table below reveals that `OUTAGE.DURATION` varies significantly across `CLIMATE.REGION` and `CLIMATE.CATEGORY`, with regions like East North Central experiencing notably longer outages in colder and normal climates, while the Southwest shows much higher outage durations in warm climates. These insights help identify which climate conditions and regions are more prone to prolonged outages, guiding targeted strategies for improving power grid resilience.

| CLIMATE.REGION     |      cold |    normal |      warm |
|:-------------------|----------:|----------:|----------:|
| Central            |   3033.18 |   2910.41 |   2413.84 |
| East North Central |   6568.79 |   5336.3  |   3022.12 |
| Northeast          |   4296.38 |   2497.17 |   4175.91 |
| Northwest          |   1141.94 |    876.76 |   3186.08 |
| South              |   2049.31 |   3787.81 |   1861.4  |
| Southeast          |   1745.86 |   2392.27 |   2605.58 |
| Southwest          |    599.05 |    303.02 |   5127.68 |
| West               |   1762.71 |   1264.71 |   2044.23 |
| West North Central |    250    |     33.17 |   2486.5  |

The pivot table below has the same paramaters as the table above, however, it represents a joint distribution of `OUTAGE.DURATION` between `CLIMATE.REGION` and `CLIMATE.CATEGORY`. The table shows that normal climates see the highest number of outages across most regions, with the Northeast, Central, and South being affected the most. This indicates that energy companies should focus on improving grid resilience in these regions and consider weather patterns and infrastructure quality as key risk factors for predicting and mitigating severe outages.

| CLIMATE.REGION     |   cold |   normal |   warm |
|:-------------------|-------:|---------:|-------:|
| Central            |     60 |       94 |     25 |
| East North Central |     38 |       81 |     17 |
| Northeast          |    103 |      163 |     43 |
| Northwest          |     36 |       41 |     25 |
| South              |     55 |      108 |     53 |
| Southeast          |     44 |       71 |     33 |
| Southwest          |     20 |       43 |     22 |
| West               |     63 |       84 |     57 |
| West North Central |      4 |        6 |      4 |

# Assessment of Missingness

## NMAR Analysis

There are many columns in the dataset that contain missing values. However, one column that I believe is likely Not Missing At Random (NMAR) is `DEMAND.LOSS.MW`. This might be due to circumstances during particularly severe outages, where the peak demand loss was not recorded accurately or at all because personnel that record the data could have been compromised or overwhelmed. Additionally, if the demand loss was very high or very low, the data was more likely to be left out due to reporting biases or difficulties. The absence of data in `DEMAND.LOSS.MW` is directly related to the severity of the power outage event, which means the missingness is tied to the values that this variable would take if they were observed. Additional data I'd want to obtain to make the missingness Missing At Random (MAR) would be information on the data collection practices during outages, such as protocols followed by utility companies, which can reveal if certain types of outages are less likely to have complete data.

## Missingness Dependency

In this part, I am going to test if the missingness of `TOTAL.SALES` depends on other columns. The two other columns that I used are `MONTH` and `NERC.REGION`. The significance level that I chose for both permutation tests is 0.05, and the test statistic if Total Variance Distance (TVD).

First, I perform the permutation test on `TOTAL.SALES` and `MONTH`, and test to see if the missingness of `TOTAL.SALES` does depend on `MONTH`.

**Null Hypothesis**: Distribution of `MONTH` when `TOTAL.SALES` is missing is the same as the distribution of `MONTH` when `TOTAL.SALES` is not missing.

**Alternative Hypothesis**: Distribution of `MONTH` when `TOTAL.SALES` is missing is NOT the same as the distribution of `MONTH` when `TOTAL.SALES` is not missing.

Below is the observed distribution of `MONTH` when `TOTAL.SALES` is missing and not missing.

| MONTH | total_sales_missing = False | total_sales_missing = True |
|-------|------------------------------|-----------------------------|
| 1     | 0.0899471                    | nan                         |
| 2     | 0.0899471                    | nan                         |
| 3     | 0.0661376                    | nan                         |
| 4     | 0.0734127                    | nan                         |
| 5     | 0.0839947                    | nan                         |
| 6     | 0.128968                     | nan                         |
| 7     | 0.111111                     | 1                           |
| 8     | 0.10119                      | nan                         |
| 9     | 0.0621693                    | nan                         |
| 10    | 0.0720899                    | nan                         |
| 11    | 0.047619                     | nan                         |
| 12    | 0.0734127                    | nan                         |

After I performed permutation tests, I found that the **observed statistic** for this permutation test is: 0.4444444444444444, and the **p-value** is 0. The plot below shows the empirical distribution of the TVD for the test.
<iframe
  src="assets/tvd-month-sales.html"
  width="800"
  height="600"
  frameborder="0"></iframe>
Since the p-value is less than the 0.05 significance level, we reject the null hypothesis. Therefore, the missingness of `TOTAL.SALES` does depend on `MONTH`.

Second, I perform the permutation test on `TOTAL.SALES` and `NERC.REGION`, and the missingness of `TOTAL.SALES` does not depend on `NERC.REGION`.

**Null Hypothesis**: Distribution of `NERC.REGION` when `TOTAL.SALES` is missing is the same as the distribution of `NERC.REGION` when `TOTAL.SALES` is not missing.

**Alternative Hypothesis**: Distribution of `NERC.REGION` when `TOTAL.SALES` is missing is NOT the same as the distribution of `NERC.REGION` when `TOTAL.SALES` is not missing.

Below is the observed distribution of `NERC.REGION` when `TOTAL.SALES` is missing and not missing.

| NERC.REGION   | total_sales_missing = False | total_sales_missing = True |
|:--------------|------------------------------|-----------------------------|
| ASCC          | nan                          | 0.0454545                   |
| ECAR          | 0.0224868                    | nan                         |
| FRCC          | 0.0284392                    | 0.0454545                   |
| FRCC, SERC    | 0.000661376                  | nan                         |
| HECO          | 0.00198413                   | nan                         |
| HI            | 0.000661376                  | nan                         |
| MRO           | 0.0297619                    | 0.0454545                   |
| NPCC          | 0.0992063                    | nan                         |
| PR            | 0.000661376                  | nan                         |
| RFC           | 0.274471                     | 0.181818                    |
| SERC          | 0.130952                     | 0.318182                    |
| SPP           | 0.0429894                    | 0.0909091                   |
| TRE           | 0.0720899                    | 0.0909091                   |
| WECC          | 0.295635                     | 0.181818                    |

After we performed permutation tests, we found that the **observed statistic** for this permutation test is: 0.24657287157287155, and the **p-value** is 0.101. The plot below shows the empirical distribution of the TVD for the test.
<iframe
  src="assets/tvd-nerc-sales.html"
  width="800"
  height="600"
  frameborder="0"></iframe>

Since the p-value is greater than the 0.05 significance level, we fail to reject the null hypothesis. Therefore, the missingness of `TOTAL.SALES` does not depend on `NERC.REGION`.

# Hypothesis Testing

In my hypothesis test, I used a permutation test because I wanted to check whether the two distributions look like they were drawn from the same population distribution. In my test, I proposed that **higher electricity consumption (high sales) leads to higher demand loss in megawatts (MW) compared to lower electricity consumption (low sales)**. In this case, different levels of `TOTAL.SALES` are defined as High Sales (>= `TOTAL.SALES`.median()) and Low Sales (< `TOTAL.SALES`.median()). This investigation is important for understanding the relationship between electricity consumption and the severity of power outages. Energy companies could then consider electricity consumption levels as a risk factor when predicting the severity and location of future power outages. I chose the difference in group means as my test statistic instead of the absolute difference in group means because I am interested in the direction of the relationship. Specifically, I want to determine if higher electricity consumption (high sales) is associated with greater demand loss in megawatts compared to lower electricity consumption (low sales).

**Null Hypothesis (H0)**: There is no significant difference in the distribution of `DEMAND.LOSS.MW` across different levels of `TOTAL.SALES`.

**Alternative Hypothesis (H1)**: Higher levels of `TOTAL.SALES` are associated with greater `DEMAND.LOSS.MW`.

**Test Statistic**: Difference in group means between `DEMAND.LOSS.MW` of high and low levels of `TOTAL.SALES`.

**Significance Level**: Standard 0.05

After performing permutation tests with 10,000 simulations, I found that the **observed difference** is 326.1661476961919 and the **p-value** is 0.0455. The plot below shows the empirical distribution of the test statistic for the permutation test.
<iframe
  src="assets/hypothesis-test.html"
  width="800"
  height="600"
  frameborder="0"></iframe>

## Conclusion of Permutation Test
Since the p-value I found (0.0455) is less than the standard significance level of 0.05, I reject the null hypothesis. This suggests that there is a statistically significant difference in the distribution of `DEMAND.LOSS.MW` across different levels of `TOTAL.SALES`. In other words, the evidence indicates that the demand loss during power outages tends to be associated with the level of total electricity sales. The observed difference in demand loss between high sales and low sales areas suggests a potential relationship where higher electricity consumption levels (as measured by total sales) might be related to greater demand loss during outages. This finding implies that electricity consumption levels could be a relevant factor when predicting the severity of power outages.

# Framing a Prediction Problem

My model will predict the energy consumption of an area. This will be a regression problem, as the goal is to predict a continuous variable, which is the electricity consumption in a given area. The response variable that I'm going to predict is `TOTAL.SALES`, which represents the total electricity consumption in an area measured in megawatt-hours (MWh). I chose this variable because it directly reflects the amount of electricity consumed, which is crucial for energy companies to plan for supply, distribution, and infrastructure needs. 

The metric I am using to evaluate the model is R-squared (R<sup>2</sup>) because it provides an indication of how well the model fits the data. R<sup>2</sup> measures the proportion of the variance in the dependent variable that is predictable from the independent variables. A higher R<sup>2</sup> indicates a better fit of the model to the data.

At the time of prediction, we would know geographical locations (`POSTAL.CODE`, `NERC.REGION`, `PCT_WATER_INLAND`, `AREAPCT_URBAN`), timage (`YEAR`, `MONTH`, `IS_DARK`), climate (`CLIMATE.REGION`), and economic attributes (`PC.REALGSP.STATE`, `POPULATION`, `IND.CUSTOMERS`). This information will allow us to predict the energy consumption of a given area.

# Baseline Model

My model is a linear regression model using the features `YEAR` (ORDINAL), `MONTH` (ORDINAL), `CLIMATE.REGION` (NOMINAL), `PC.REALGSP.STATE` (QUANTITATIVE), `NERC.REGION` (NOMINAL), `POPULATION` (QUANTITATIVE), `PCT_WATER_INLAND` (QUANTITATIVE), `POSTAL.CODE` (NOMINAL) to predict the energy consumption of an area. To prepare the data for modeling, we performed the following steps: Standardized the quantitative features (`PC.REALGSP.STATE`, `POPULATION`, `PCT_WATER_INLAND`) using StandardScaler to normalize the data, ensuring all features have a mean of 0 and a standard deviation of 1, and Applied one-hot encoding to the nominal features (`CLIMATE.REGION`, `NERC.REGION`, `POSTAL.CODE`) using OneHotEncoder to convert categorical variables into a format suitable for regression by creating binary columns for each category. After training the model, I evaluated its performance using the R-squared (R<sup>2</sup>) metric and RMSE metric. The result was R-squared (R<sup>2</sup>): 0.8774 and an RMSE of approximately 2343285.3, which is a 20.14% relative error based on `TOTAL.SALES`'s mean. Given the high R-squared value, we can see that the features explain a good amount of the variance in `TOTAL.SALES`, however, the high relative error in RMSE, means we can improve on this model.

# Final Model

For the final model, I incorporated two additional features: `POP.DENSITY.URBAN` (Population Density in Urban Areas) and `AVG.MONTHLY.PRICE` (Average Monthly Electricity Price). I added `POP.DENSITY.URBAN` because urban areas with higher population densities typically experience heightened residential and commercial activity, directly impacting electricity demand. I also added `AVG.MONTHLY.PRICE` because it offers insights into consumption behavior, revealing the price sensitivity of demand and how fluctuations in electricity prices influence overall sales.

I used the RandomForestRegressor model and GridSearchCV with 5-fold cross-validation to find the optimal RandomForestRegressor model configuration that maximizes the R-squared score. The hyperparameters that I ended up using were
 - 200 trees (n_estimators)
 - maximum depth of 20 (max_depth)

In contrast, the baseline model employed a Linear Regression model with default parameters and no hyperparameter tuning.

The final model significantly improved compared to the baseline model by adding relevant features `POP.DENSITY.URBAN` and `AVG.MONTHLY.PRICE`, using a better modeling fit (RandomForestRegressor), and optimized hyperparameters. This led to a more accurate prediction, evidenced by a higher R-squared (R<sup>2</sup>) value as the final model got a R-squared (R<sup>2</sup>) value of 0.9926, and reduced RMSE by 73.2% to 622,847.10 MWh. Given the scale of `TOTAL.SALES` (around 11.63 million MWh on average), a 5.4% relative error is quite reasonable. These improvements indicate that the final model captures a greater portion of the variance in `TOTAL.SALES` and captures more of the complex relationships in the data much better than the baseline model, resulting in more precise predictions.

# Takeaways

...



<!-- 
# Fairness Analysis
My groups for the fairness anal

To perform a fairness analysis of your final model, we'll compare its performance across two groups. In this case, let's define the groups based on the REGION attribute: "Urban" and "Rural" areas. We'll use R-squared (R<sup>2</sup>) as our evaluation metric since your task involves regression.

**Null Hypothesis**: The model is fair. Its (R<sup>2</sup>) score for Urban and Rural areas are roughly the same, and any differences are due to random chance.

**Alternative Hypothesis**: The model is unfair. Its (R<sup>2</sup>) score for Urban areas is different from its (R<sup>2</sup>) score for Rural areas.

1) Compute the actual difference in (R<sup>2</sup>) scores between the Urban and Rural groups using the final fitted model.
2) Permute the REGION labels multiple times and compute the difference in (R<sup>2</sup>) scores for each permutation.
3) Compare the actual difference to the distribution of differences from the permutations to determine the p-value.

My groups for the fairness analysis are longer vs shorter outages. This is defined as outages that are greater than 3000 minutes, vs outages that are less than 3000 minutes.

I decided on these groups because the cause category (which is predicted by my model) can greatly determine the outage duration. We want to make sure that the model can predict the classification well because this can inform energy companies on what to focus on to prevent longer outages.

My evaluation metric will be F1 score since the classes (longer vs shorter) are imbalanced, and this metric accounts for that imbalance, while also incorporating the precision and recall. I will use permutation tests to calculate the F1 score for longer vs shorter outages (that are randomly shuffled) and then compare this absolute difference to my initial observed absolute difference.

Null Hypothesis: The model is fair. Its F1 scores for longer and shorter outages are roughly the same, and any differences are due to random chance.

Alternative Hypothesis: The model is unfair. Its F1 score for longer outages is significantly different from the F1 score for shorter outages.

I performed a permutation test with 10000 trials. My significance level is the standard 0.05, and I got a p_value of 0.0 so because this is below the significance level, I reject the null hypothesis. The model is significantly different in terms of F1 score for longer vs shorter outages.

The figure below shows the distribution of the statistic. -->


