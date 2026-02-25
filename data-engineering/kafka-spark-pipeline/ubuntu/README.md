> [!IMPORTANT]
> The upcoming code considers `$HOME/pipeline` as working directory therefore it is suggested to first run the following code snippet
> ```
> cd $HOME
> mkdir pipeline && cd pipeline
> ```
> and then copy the files contained in [scripts](./scripts) into it.

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

```

## Kafka 
- Version
  - The employed Kafka version is 2.13-4.1.1. 
    ```
    mkdir app && cd $HOME/app
    curl -O https://archive.apache.org/dist/kafka/4.1.1/kafka_2.13-4.1.1.tgz
    tar -xvzf kafka_2.13-4.1.1.tgz
    rm kafka_2.13-4.1.1.tgz
    sudo mv kafka_2.13-4.1.1 /opt/kafka
    ```
- Configuration
  - Setting up a 3-nodes Kafka cluster
    ```
    ./cluster_setup.sh 3
    ```
  - Creating _tweet-train_ and _tweet-test_ with `partitions==2`and `replication-factor==2`
    ```
    ./topic_setup.sh 3 2 2
    ```
## Ingesting training data
