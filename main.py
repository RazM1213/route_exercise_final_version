from pipeline import Pipeline
from read.rabbit_mq.rabbit_mq_reader import RabbitMqReader
from transform.student.student_transformer import StudentTransformer
from write.folder.folder_writer import FolderWriter


def main():
    pipeline = Pipeline(RabbitMqReader(), FolderWriter(), StudentTransformer())

    pipeline.run()


if __name__ == "__main__":
    main()
