import os
import re
import pyspark
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType


class DataPreparing:

    def __init__(self, spark, path) -> None:
        self.spark = spark
        self.path = path
        self.preparing_df = self.prepare_df(self.path)

    def run(self):
        clear_df = self.clear_df(self.preparing_df)
        self.save_to_parquet(clear_df)

    def prepare_df(self, path_to_file: str) -> pyspark.sql.dataframe.DataFrame:
        rdd = self.spark.sparkContext.textFile("{0}".format(self.path))
        header = rdd.take(1)[0]  # достаем заголовок
        df = (
            rdd.filter(lambda r: r != header)
            .map(lambda r: r.split(","))
            .toDF(re.sub(r"\s+", "", header).split("|"))
        )
        # корректируем нейминг
        df = df.withColumnRenamed("#tranaction_id", "transaction_id")
        # меняем тип колонки string -> float
        df = df.withColumn(
            "tx_amount", df["tx_amount"].cast(FloatType())
        )
        return df

    @staticmethod
    def clear_df(
        df: pyspark.sql.dataframe.DataFrame,
    ) -> pyspark.sql.dataframe.DataFrame:
        # оставляем только уникальные строки
        df = df.dropDuplicates()
        # убираем нулы
        for column in df.columns:
            df = df.where(F.col(column).isNotNull())
        # оставляем положительные значения
        df = df.where((F.col("tx_amount") > 0) & (F.col("tx_time_seconds") > 0))
        return df

    def save_to_parquet(self, df: pyspark.sql.dataframe.DataFrame) -> None:
        name_for_parquet = self.path.split("/")[-1]
        print(name_for_parquet)
        df.write.parquet(f"clear_data/{name_for_parquet}.parquet")
