import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.{ArrayType, StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext, rdd}

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

val conf = new SparkConf().setAppName("Devoir2").setMaster("local")
val sc = new SparkContext(conf)
val spark = SparkSession.builder().config(conf).getOrCreate();
val path = "/home/gableb/bddreparties/Devoir2/Exercice1/crawler/scala_readable.json"

val myDataFrame = spark.read.json(path)
myDataFrame.printSchema()

myDataFrame.show()

val myCreatureArray = myDataFrame.distinct()
  .collect()
  .map{ row:Row =>
      (row.getAs[String]("name"), row.getAs[mutable.WrappedArray[String]]("spells").array)
  }

var creatures = sc.parallelize(myCreatureArray)

creatures.take(5).foreach(println)

var mapped = creatures.flatMap(elem => {
    val results = new ArrayBuffer[(String, Array[String])]
    for (spellname <- elem._2) { // Pour chaque sort d'une créature
        results += Tuple2(spellname, Array(elem._1)) // Emit (nomdusort, [nomdelacréature])
    }
    results
})

var reduced = mapped.reduceByKey((a, b) => {
    a ++ b //Concaténer les tableaux de noms
})

def printSpellCreatures(spell: (String, Array[String])): Unit ={
    print(spell._1 + " : ");
    println(spell._2.mkString(", "));
}

reduced.take(5).foreach(printSpellCreatures)

val serialized = reduced.map(x => (x._1, x._2.mkString("; ")))
serialized.take(5).foreach(println)
serialized.saveAsTextFile("/home/gableb/bddreparties/Devoir2/Exercice1/output_rdd")

spark.createDataFrame(reduced).toDF("spell", "creatures").write.format("json").save("/home/gableb/bddreparties/Devoir2/Exercice1/output_json");