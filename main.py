from config.rabbit_mq_config import QUEUE, SECOND_QUEUE
from pipeline import Pipeline
from read.kafka.kafka_reader import KafkaReader
from read.rabbit_mq.rabbit_mq_reader import RabbitMqReader
from transform.student.student_transformer import StudentTransformer
from write.elastic.elastic_writer import ElasticWriter
from write.folder.folder_writer import FolderWriter


def main():
    pipeline = Pipeline(
        ElasticWriter(),
        StudentTransformer(),
        KafkaReader()
        # [RabbitMqReader(queue=QUEUE), RabbitMqReader(queue=SECOND_QUEUE)]
    )

    pipeline.run()


if __name__ == "__main__":
    main()
