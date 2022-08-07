import json

from consts.consts import DECODE_FORMAT
from read.reader import Reader
from transform.transformer import Transformer
from write.writer import Writer


class Pipeline:
    def __init__(self, writer: Writer, StudentTransformer: Transformer, *readers: Reader):
        self.readers = readers
        self.writer = writer
        self.StudentTransformer = StudentTransformer

    def callback(self, body):
        string_body = body.decode(DECODE_FORMAT)
        json_body = json.loads(string_body)
        try:
            output = self.StudentTransformer.parse_output(json_body)
            if output is not None:
                self.writer.write(output)
        except Exception as ex:
            print(ex)

    def run(self):
        for reader in self.readers[0]:
            reader.listen(callback=self.callback)
