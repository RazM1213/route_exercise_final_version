import json
import threading

from kafka.consumer.fetcher import ConsumerRecord

from consts.consts import DECODE_FORMAT
from read.reader import Reader
from transform.transformer import Transformer
from write.writer import Writer


class Pipeline:
    def __init__(self, writer: Writer, transformer: Transformer, *readers: Reader):
        self.readers = readers
        self.writer = writer
        self.transformer = transformer

    def callback(self, body):
        if type(body) == ConsumerRecord:
            json_body = json.loads(body.value.decode(DECODE_FORMAT))
        else:
            json_body = json.loads(body)

        try:
            output = self.transformer.parse_output(json_body)
            if output is not None:
                self.writer.write(output)
        except Exception as ex:
            print(ex)

    def run(self):
        if type(self.readers[0]) == list:
            if len(self.readers[0]) > 1:
                threads = []
                for reader in self.readers[0]:
                    threads.append(threading.Thread(target=reader.listen, args=[self.callback]))

                for thread in threads:
                    thread.start()
        else:
            self.readers[0].listen(callback=self.callback)
