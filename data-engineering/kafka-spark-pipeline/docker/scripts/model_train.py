# Importing packages
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer
import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.ml import Pipeline
import os
import sys
import time

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
    .read\
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)\
    .option("subscribe", "tweet-train")\
    .load()

""" Benchmarking code
start_read = time.time()
row_count = df.cache().count()
end_read = time.time()
print(f"Elapsed time: {end_read-start_read}")
"""

# Converting data from binary to string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING) as text")
print(df.show(n=100))

# Pipeling building
document_assembler = DocumentAssembler() \
    .setInputCol("text")\
    .setOutputCol("document")

embeddings = UniversalSentenceEncoder.pretrained(name="tfhub_use", lang="en")\
    .setInputCols(["document"])\
    .setOutputCol("embeddings")\

dl = ClassifierDLApproach()\
    .setInputCols(["embeddings"])\
    .setOutputCol("class")\
    .setLabelColumn("key")\
    .setMaxEpochs(25)\
    .setEnableOutputLogs(True)

finisher = Finisher()\
    .setInputCols(["class"])\
    .setOutputCols(["prediction"])\
    .setOutputAsArray(False)

indexer = StringIndexer()\
    .setInputCols(["key", "prediction"])\
    .setOutputCols(["key_index", "pred_index"])\
    .setStringOrderType("alphabetAsc")\
    .setHandleInvalid("keep")

pipeline = Pipeline()\
    .setStages([
    document_assembler,
    embeddings,
    dl,
    finisher,
    indexer,
])

# Fitting the pipeline
result = pipeline.fit(df)

# Saving the model weights
result.write().overwrite().save("/pipeline/data/model_weights")

# Applying the pipeline results to the df
result = result.transform(df)

# Printing to console the dataset with the predicted label
result.selectExpr("key", "text", "prediction").show(n=100)

# Printing accuracy, recall and precision metrics
accuracy = MulticlassClassificationEvaluator(labelCol="key_index", predictionCol="pred_index", metricName="accuracy")
acc = accuracy.evaluate(result)
print(f"Accuracy: {acc:.2%}")

recall = MulticlassClassificationEvaluator(labelCol="key_index", predictionCol="pred_index", metricName="weightedRecall")
rec = recall.evaluate(result)
print(f"Recall: {rec:.2%}")

precision = MulticlassClassificationEvaluator(labelCol="key_index", predictionCol="pred_index", metricName="weightedPrecision")
pre = precision.evaluate(result)
print(f"Precision: {pre:.2%}")