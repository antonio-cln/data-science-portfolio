> [!IMPORTANT]
> The upcoming code considers `$HOME/pipeline` as working directory therefore it is suggested to first run the following code snippet
> ```
> cd $HOME
> mkdir pipeline && cd pipeline
> ```
> and then copy the files contained in [scripts](./scripts) into it. The Kaggle dataset is then required to be downloaded and placed in `$HOME/pipeline` aswell.
>
> Proceed to then make the `.sh` and `.py` file executable
> ```
> 
> ```

## Environment setup
- Operative System
  - The OS employed for this pipeline implementation is Ubuntu version 24.04
- Python
  - Ubuntu 24.04 provides by default Python version 3.12.3, which is the version employed
- Java
  - Java is required by both Kafka and Spark to work properly. The employed Java version is 17.0.17
    ```
    sudo apt install openjdk-17-jdk -y
    ```

## Python requirements
The required Python packages are provided in the [requirements.txt](./requirements.txt) file.
```
python3 -m venv pipe-venv
source pipe-venv/bin/activate
pip install -r requirements.txt
```

## Kafka cluster and topics
- The employed Kafka version is 2.13-4.1.1. 
  ```
  curl -O https://archive.apache.org/dist/kafka/4.1.1/kafka_2.13-4.1.1.tgz
  tar -xvzf kafka_2.13-4.1.1.tgz
  rm kafka_2.13-4.1.1.tgz
  sudo mv kafka_2.13-4.1.1 /opt/kafka
  ```
- Configuration
  - Setting up a 3-nodes Kafka cluster
    ```
    ./kafka/cluster_setup.sh 3
    ```
  - Creating _tweet-train_ and _tweet-test_ with `partitions==2`and `replication-factor==2`
    ```
    ./kafka/topic_setup.sh 3 2 2
    ```
    
## Data preparation and training data ingestion
- Performing data preparation and then ingestion through the 3-nodes Kafka cluster
  ```
  python ./data-preparation/producer_train.py 3
  ```
  
## Spark model training
- Reading data in batch from the _tweet-train_ topic of the 3-nodes Kafka cluster, training a Spark NLP model and saving weights locally
  ```
  ./spark/model_train.sh 3
  ```
  
## Spark prediction
- Setting up Spark NLP model based on the weights of the previously trained model and preparing it to receive streaming data from the _tweet-test_ topic of the 3-nodes Kafka cluster
  ```
  ./spark/model_test.sh 3
  ```

## Testing data ingestion
- Performing data ingestion through the 3-nodes Kafka cluster
  ```
  python ./data-preparation/producer_test.py 3
  ```








