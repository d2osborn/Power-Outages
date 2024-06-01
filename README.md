# Power Outages Energy Consumption Statistical Analysis
Power outage energy consumption statistical analysis is an extensive data science project. It involves several stages of statistical analysis, from data cleaning and exploratory data analysis to assessing missingness, hypothesis testing, framing a prediction problem (its baseline and final model), and a fairness analysis. This project aims to deduce the most influential characteristics of a major power outage, and how it can help energy companies lead to more efficient allocation of resources, reduced economic losses, and increased safety for individuals and infrastructure.

Author: Diego Osborn

## Introduction
One major issue that's constantly being faced globally is the occurrence of power outages. Power outages pose a problem because they can disrupt daily life, impact critical services, pose safety risks, and result in economic losses for individuals, businesses, and communities. The dataset I will be working on is the data that was used in an article by Sayanti Mukherjee et al., "A Multi-Hazard Approach to Assess Severe Weather-Induced Major Power Outage Risks in the U.S.", and can be accessed from Purdue University’s Laboratory for Advancing Sustainable Critical Infrastructure, at https://engineering.purdue.edu/LASCI/research-data/outages.

This dataset covers major power outages--affecting at least 50,000 customers or causing an unplanned firm load loss of at least 300 MW--in the U.S. from January 2000 to July 2016, which includes several important features such as geographical location, timing, climatic conditions, land-use characteristics, electricity consumption, and economic attributes of the affected states.

The central question I am interested in is: **What are the characteristics of major power outages with higher severity?** I want to use data analysis to understand which characteristics have the highest impact on major power outages, and using this knowledge I can set up a model that predicts the energy consumption of an area. Accurately predicting the energy consumption levels of an area allows energy companies to effectively manage and allocate resources, ensuring a stable and reliable supply of electricity. Leading to more reliable electricity services, reduced economic losses, and increased safety for individuals and infrastructure.

The dataset, outage, contains 1534 rows, each being a unique record of a major power outage, with 56 columns. Here's a brief description of some of the columns that are relevant to my analysis:

- `gameid`: This column represents a unique identifier for each individual match played. It allows us to distinguish between different matches in the dataset.

- `YEAR`: Indicates the year when the outage event occurred

- `U.S._STATE`: Represents all the states in the continental U.S.

- `NERC.REGION`: The North American Electric Reliability Corporation (NERC) regions involved in the outage event

- `CLIMATE.REGION`: U.S. Climate regions as specified by National Centers for Environmental Information (nine climatically consistent regions in continental U.S.A.)

- `OUTAGE.DURATION`: Duration of outage events (in minutes)

- `DEMAND.LOSS.MW`: Amount of peak demand lost during an outage event (in Megawatt) [but in many cases, total demand is reported]

- `CUSTOMERS.AFFECTED`: Number of customers affected by the power outage event

- `RES.PRICE`: Monthly electricity price in the residential sector (cents/kilowatt-hour)

- `COM.PRICE`: Monthly electricity price in the commercial sector (cents/kilowatt-hour)

- `TOTAL.SALES`: Total electricity consumption in the U.S. state (megawatt-hour)

- `PC.REALGSP.STATE`: Per capita real gross state product (GSP) in the U.S. state (measured in 2009 chained U.S. dollars)

- `POPULATION`: Population in the U.S. state in a year
