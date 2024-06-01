# Power Outages Energy Consumption Statistical Analysis
League of Legends First Blood Statistical Analysis is a comprehensive data science project conducted at UCSD. The project encompasses various stages of analysis, starting from exploratory data analysis to hypothesis testing, creation of baseline models, and concluding with fairness analysis. The primary focus of the project is to investigate the significance of the "first blood" event in League of Legends matches and its impact on match statistics and outcomes.

Authors: Sirui Zhang, Krystal Qiu

## Introduction
### General Introduction
League of Legends (LOL) is a popular multiplayer online battle arena (MOBA) game developed by Riot Games. With millions of players worldwide, it has become one of the most influential and widely played esports in the gaming industry. The data set we will be working with is a professional data set that’s developed by Oracle's Elixir. The file records match data from professional LOL esports gaming matches throughout 2022. 

This dataset captures key gameplay statistics and outcomes from a collection of LOL matches, offering a rich source of information for understanding player behavior, team dynamics, and match outcomes. It includes a variety of features such as individual player performance, team strategies, in-game statistics, and overall match dynamics.

In the realm of League of Legends (LOL), the concept of **"first blood"** holds significant weight and serves as an important trajectory of a match. First blood refers to the initial first kill secured by a team during the early stages of a game. Beyond its immediate impact on the scoreboard, first blood sets the tone for the ensuing gameplay, often shaping the general dynamics, strategies, and outcomes of the match.

The central question we are interested in is **In what degree of effectiveness does the firstblood status has to other gaming statistics in the data set**. We want to use data analysis techniques to testify the impact of first blood on gaming statistics,  including individual player performance, team strategies, in-game metrics, and ultimately, match outcomes. And therefore using these statistics to set up a prediction model to predict the positions of the players. This predictive model holds immense potential to enhance strategic decision-making, optimize team compositions, and elevate overall gameplay experience.

### Introduction of Columns
The dataset introduces a comprehensive array of columns featuring gameplay metrics and match outcomes from professional League of Legends esports matches. Ther are 148992 rows in this dataset, and here's an introduction to some of the key columns:
In the dataset provided, we encounter various columns that encapsulate essential gameplay statistics and match outcomes from professional League of Legends (LoL) esports matches. Here's a brief introduction to each of these columns:

- `gameid`: This column represents a unique identifier for each individual match played. It allows us to distinguish between different matches in the dataset.

- `side`: The 'side' column denotes the team affiliation of a particular player or team. It typically distinguishes between 'blue' and 'red' teams.

- `result`: This column indicates the outcome of a match for a specific team or player. 1 indicates the team or the team that the player is in won, 0 indicates lost.

- `kills`: The 'kills' column quantifies the number of enemy champions a player or team successfully eliminated during the match. 

- `deaths`: Conversely, the 'deaths' column records the number of times a player or team was eliminated by enemy champions. 

- `assists`: The 'assists' column records the number of assists credited to a player or team, indicating instances where they contributed to eliminating an enemy champion without securing the kill themselves.

- `firstblood`: This binary column indicates 1 if a player gets the first blood, or assists to get the first blood.
- 
- `firstbloodkill`: Similar to 'firstblood', this binary column specifically denotes whether a player or team secured the first kill of the match, thereby earning the distinction of 'first blood.'

- `monsterkills`: the number of monsters or neutral objectives slain by a team or player during a game. These monsters can include jungle camps, epic monsters like Baron Nashor or the Dragon, as well as other neutral objectives such as Rift Herald or elemental drakes. The number of monster kills can be indicative of a team's control over the map, their ability to secure key objectives, and their overall dominance in the game.

- `position`: The 'position' column specifies the role or position played by an individual player within their team composition. Common positions include 'top,' 'jungle,' 'mid,' 'bot,' and 'support.'

- `minionkills`: This column records the number of minions or neutral monsters slain by a player or team during the match. It reflects their ability to efficiently farm gold and experience points, crucial for character progression and itemization.

- `league`: The 'league' column denotes the specific league tournament in which the match took place.
