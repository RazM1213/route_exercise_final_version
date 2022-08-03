import datetime
import json
import logging
from dataclasses import asdict

import coloredlogs
from elasticsearch import Elasticsearch

from config import elastic_config
from consts.formats import DATETIME_FORMAT, ELASTIC_DATETIME_FORMAT
from models.output import Output
from write.elastic.mapping import mapping
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
        json_query = json.loads(query)
        json_query["birthDate"] = datetime.datetime.strptime(json_query["birthDate"], DATETIME_FORMAT).strftime(ELASTIC_DATETIME_FORMAT)

        index = datetime.datetime.strptime(output.birthDate, DATETIME_FORMAT).year

        if index not in ElasticWriter.get_elastic_client().indices.get(index='*').body.keys():
            ElasticWriter.get_elastic_client().indices.create(
                index=f"{index}",
                body=mapping
            )

        ElasticWriter.get_elastic_client().index(
            index=f"{index}",
            document=json.dumps(json_query),
            id=output.studentDetails.id
        )

        coloredlogs.install()
        logging.info(f"[X] Created a document in elasticsearch for: {output.studentDetails.fullName}")
