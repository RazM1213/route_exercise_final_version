from pipeline import Pipeline
from read.kafka.kafka_reader import KafkaReader
from read.rabbit_mq.rabbit_mq_reader import RabbitMqReader
from transform.student.student_transformer import StudentTransformer
from write.elastic.elastic_writer import ElasticWriter


def main():
    pipeline = Pipeline(
        ElasticWriter(),
        StudentTransformer(),
        [RabbitMqReader(), KafkaReader()]
    )

    pipeline.run()


if __name__ == "__main__":
    main()
