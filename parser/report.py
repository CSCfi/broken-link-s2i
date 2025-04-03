from datetime import date
import xml.etree.ElementTree as ET

from .result import Result


class Report:
    NOT_FOUND_RESULT = "404 Not Found"
    NOT_FOUND_XPATH = f"./urldata/*[@result='{NOT_FOUND_RESULT}']/.."
    XML_TAGS = ("url", "name", "parent")

    def __init__(self, input_filename):
        self.xml_tree_root = ET.parse(input_filename).getroot()
        self.month = date.today().strftime("%B %Y")

    @staticmethod
    def __get_xml_text(elem, tag):
        return elem.find(tag).text

    @classmethod
    def __parse_xml_result(cls, elem):
        return tuple(cls.__get_xml_text(elem, tag)
                     for tag in cls.XML_TAGS)

    @property
    def results(self):
        xml_results = self.xml_tree_root.findall(self.NOT_FOUND_XPATH)

        return [Result(*(*self.__parse_xml_result(result),
                         self.NOT_FOUND_RESULT))
                for result in xml_results]

    def __write_markdown(self, fp):
        md_results = f"## Broken links, {self.month}\n" \
            + "".join(result.markdown for result in self.results)
        fp.write(md_results)

    def __write_txt(self, fp):
        results = "".join(result.txt for result in self.results) \
            + f"\nProcessed: {len(self.results)}"
        fp.write(results)

    def to_file(self, output_filename):
        with open(output_filename, "wt", encoding="utf-8") as output_file:
            if output_filename.endswith(".md"):
                self.__write_markdown(output_file)
            else:
                self.__write_txt(output_file)
