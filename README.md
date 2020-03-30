## Recommendation on Game Release Season
My overall objective of this prpject was to be able to recommend the best time of year to a relase in order to obtain the best revenue by looking at the relese dates and revenues of similar games.


## Data Collecting and Cleaning - noteboook 
The first notebook will 
1. Use two different datasets from Kaggle that took game information from steam.com 
2. We will do slight cleaning on each dataset then merge them to make one
3. Further cleaning will be done on the combined dataset 
4. This dataset will then be used for out recommendation system


## Visulizations - notebook
This notebook will call in data that we cleaned in our previous notebook. Then we will play with columns to make visuals and get a better understanding of our data. 


## Recommendation System - notebook
This notebook will call in data that we cleaned in our previous notebook. We will then tranform the text data into readable form and run cosine similarities on our games. It will then recommend the best season to release a game based on similar games.



## Flask app: rec_app
The flask app will do the same as the recommendation notebook. However instead of choosing a game for our current dataset and finding similar ones, it will take in a new game from the user. 

## Data
The data used for this project are 2 kaggle datasets created from scraping Steam.com. They can be found at: 
- https://www.kaggle.com/trolukovich/steam-games-complete-dataset
- https://www.kaggle.com/nikdavis/steam-store-games
