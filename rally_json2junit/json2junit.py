from json import loads


class JsonToJUnitConverter(object):
    def __init__(self, source_json, output_junit_xml):
        self.source_json = source_json
        self.output_junit_xml = output_junit_xml
        self.dic_json = ''

    def serialize_json(self):
        self.dic_json = loads(self.source_json)
