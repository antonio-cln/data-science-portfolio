## Directory contents 📂
| Content          | Description   |
| :------------- | :------------- |
| [ubuntu](./ubuntu)  | Ubuntu pipeline implementation  |
| [docker](./docker)  | Docker pipeline implementation  |


## Pipeline Overview  
<img width="2040" height="1135" alt="Pipeline" src="https://github.com/user-attachments/assets/cd7da42f-916c-49d9-b480-eb61314c4257" />


#### Data Preparation
The dataset employed in this pipeline to act as data to be ingested is a Kaggle dataset on [tweets data](https://www.kaggle.com/datasets/tariqsays/sentiment-dataset-with-1-million-tweets). The dataset is first split into a training set for the Spark NLP model and a testing set to verify the employed model performances.

#### Kafka
Two topics, _tweet-train_ and _tweet-test_, are created to ingest data being provided by a Python script.

#### Spark
The tweets are then consumed by Spark, first processing training data provided in batch by the Python script to the _tweet-train_ topic to train a model and then processing data being provided in real-time by a different Python script to the _tweet-test_ topic.
