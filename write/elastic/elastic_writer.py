import datetime
import json
import logging
from dataclasses import asdict

import coloredlogs
from elasticsearch import Elasticsearch

from config import elastic_config
from models.output import Output
from write.writer import Writer


class ElasticWriter(Writer):

    @staticmethod
    def get_elastic_client():
        es_client = Elasticsearch(
            elastic_config.LOCAL_HOST,
            basic_auth=(elastic_config.USERNAME, elastic_config.PASSWORD)
        )

        return es_client

    def write(self, output: Output):
        query = json.dumps(asdict(output, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}), indent=4)

        ElasticWriter.get_elastic_client().index(
            index=f"{datetime.datetime.strptime(output.birthDate, '%d/%m/%Y').year}",
            document=query,
            id=output.studentDetails.id
        )

        coloredlogs.install()
        logging.info(f"[X] Created a document in elasticsearch for: {output.studentDetails.fullName}")
        # print(f"[X] Created a document in elasticsearch for: {output.studentDetails.fullName}")
