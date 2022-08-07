from pipeline import Pipeline
from read.rabbit_mq.rabbit_mq_reader import RabbitMqReader
from transform.student.student_transformer import StudentTransformer
from write.elastic.elastic_writer import ElasticWriter


def main():
    pipeline = Pipeline(RabbitMqReader(), ElasticWriter(), StudentTransformer())

    pipeline.run()


if __name__ == "__main__":
    main()
