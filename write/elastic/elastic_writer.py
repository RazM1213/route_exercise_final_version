import datetime
import json
import logging
from dataclasses import asdict

import coloredlogs
from elasticsearch import Elasticsearch

from config import elastic_config, settings
from consts.formats import DATETIME_FORMAT, ELASTIC_DATETIME_FORMAT
from consts.json_fields import BIRTHDATE
from models.output import Output
from write.writer import Writer


class ElasticWriter(Writer):

    @staticmethod
    def get_elastic_client() -> Elasticsearch:
        es_client = Elasticsearch(
            elastic_config.LOCAL_HOST,
            basic_auth=(elastic_config.USERNAME, elastic_config.PASSWORD)
        )

        return es_client

    def write(self, output: Output):
        query = json.dumps(asdict(output, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}), indent=4)

        json_query = json.loads(query)
        json_query[BIRTHDATE] = datetime.datetime.strptime(json_query[BIRTHDATE], DATETIME_FORMAT).strftime(ELASTIC_DATETIME_FORMAT)

        if settings.ENV == "test":
            ElasticWriter.get_elastic_client().index(
                index=f"test-{datetime.datetime.strptime(output.birthDate, DATETIME_FORMAT).year}",
                document=json.dumps(json_query),
                id=output.studentDetails.id,
            )
        else:
            ElasticWriter.get_elastic_client().index(
                index=f"{datetime.datetime.strptime(output.birthDate, DATETIME_FORMAT).year}",
                document=json.dumps(json_query),
                id=output.studentDetails.id,
            )

        coloredlogs.install()
        logging.info(f"[X] Created a document in elasticsearch for: {output.studentDetails.fullName}")
