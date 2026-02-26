> [!IMPORTANT]
> To ensure the following commands run correctly, first copy the [scripts/](./scripts) folder into your working directory. These scripts are required for the next steps.
> The Kaggle dataset is then required to be downloaded and replace the placeholder in [shared/](.shared) aswell.
## Custom images
- Data producer
  ```
  docker build -f .\dockerfile_data-producer -t data-producer .
  ```
- Spark processor
  ```
  docker build -f .\dockerfile_spark -t spark-processor .
  ```
## Compose
```
docker compose -f .\docker-compose.yml up -d
```
The compose file structure is composed by the following services:
- `kafka1`, `kafka2` and `kafka3`
  - Nodes in the Kafka cluster
- `kafka-ui`
  - UI to easily manage the cluster at `http://localhost:8080`
- `kafka-topics-init`
  - Creates the topics
- `train-data-producer`
  - Produces data forwarded to the _tweet-train_ topic
- `test-data-producer`
  - Produces data forwarded to the _train-train_ topic
- `spark-model-builder`
  - Builds a Spark NLP model from training data and saves the model weights
- `spark-predictor`
  - Uses previously obtained model weights for a model that aims to perform prediction on testing data
