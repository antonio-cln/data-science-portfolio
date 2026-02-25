# Importing packages
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.ml import PipelineModel
import os
import sys

# Defining a class to calculate global accuracy
class GlobalAcc:
    def __init__(self):
        self.total_correct = 0
        self.total_count = 0

    def update(self, batch_correct, batch_count):
        self.total_correct += batch_correct
        self.total_count += batch_count

    def get_global_acc(self):
        if self.total_count == 0: return 0.0
        return self.total_correct / self.total_count

# Instatiating a global accuracy object
glbAcc = GlobalAcc()

# Loading model weights
model = PipelineModel.load(r"/pipeline/data/model_weights")

# Auxiliary function to evaluate metrics for each batch
def evaluate_batch(batch_df, batch_id):
    if batch_df.count() > 0:
        result = model.transform(batch_df)
        result.cache()
        batch_count = result.count()
        result.select("text", "key", "prediction").show()
        evaluator = MulticlassClassificationEvaluator(labelCol="key_index", predictionCol="pred_index")
        accuracy = evaluator.evaluate(result, {evaluator.metricName: "accuracy"})
        precision = evaluator.evaluate(result, {evaluator.metricName: "weightedPrecision"})
        recall = evaluator.evaluate(result, {evaluator.metricName: "weightedRecall"})

        batch_correct = int(accuracy * batch_count)
        glbAcc.update(batch_correct, batch_count)

        print(f"---BATCH {batch_id}---")
        print(f"Batch size: {batch_count}")
        print(f"Batch Accuracy: {accuracy:.4f}")
        print(f"Batch Precision: {precision:.4f}")
        print(f"Batch Recall: {recall:.4f}")
        print(f"Global accuracy: {glbAcc.get_global_acc():.4f}")

# Bootstrap servers variable definition
BOOTSTRAP_SERVERS = ",".join(f"kafka{i+1}:{9092 + 2*i}" for i in range(int(sys.argv[1])))

# Spark session creation
spark = SparkSession \
    .builder \
    .appName("Twittex") \
    .getOrCreate()

# Verifying versions
print(f"Spark Version: {spark.version}")
print(f"Java version: {os.popen('java -version 2>&1').read().splitlines()[0]}")
print(f"Scala version: {spark.sparkContext._jvm.scala.util.Properties.versionString()}")
print(f"Spark NLP: {sparknlp.version()}")

# Kafka read
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)\
    .option("subscribe", "tweet-test")\
    .load()

# Converting data from binary to string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING) as text")

# Printing to console the query result
out = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .foreachBatch(evaluate_batch) \
    .start()

out.awaitTermination()