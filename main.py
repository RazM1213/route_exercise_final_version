from pipeline import Pipeline
from read.kafka.kafka_reader import KafkaReader
from transform.student.student_transformer import StudentTransformer
from write.elastic.elastic_writer import ElasticWriter


def main():
    pipeline = Pipeline(
        ElasticWriter(),
        StudentTransformer(),
        KafkaReader()
    )

    pipeline.run()


if __name__ == "__main__":
    main()
