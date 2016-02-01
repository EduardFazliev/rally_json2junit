#!/usr/bin/python

import json
import sys
import logging
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

logger = logging.getLogger(__name__)

test_suite_tag = 'testsuite'
test_case_tag = 'testcase'
time_attribute = 'time'
name_attribute = 'name'
class_name_attribute = 'classname'
status_attribute = 'status'
success_status = 'success'
traceback_attribute = 'traceback'
message_attribute = 'message'
skip_status = 'skip'
skip_tag = 'skipped'
fail_status = 'fail'
fail_tag = 'failure'
failed_test_message = 'test failed'
error_status = 'error'
error_tag = 'error'


def prettify(elem):
    """ Return a pretty-printed XML string for the Element.
    Based on following article:

    https://pynlp.wordpress.com/2014/01/16/
    unit-6-part-ii-working-with-xml-files-writing-xml-files/

    :param elem: The XML tree as string
    :return: The XML tree with indentation
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    return minidom.parseString(rough_string).toprettyxml(indent="    ")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("File name is missed")
    else:
        # reading the report
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        # attempt to generate in JUnit format
        root = Element(test_suite_tag)
        root.attrib['tests'] = str(data['tests'])
        root.attrib[time_attribute] = str(data[time_attribute])
        root.attrib['success'] = str(data['success'])
        root.attrib['skipped'] = str(data['skipped'])
        root.attrib['failures'] = str(data['failures'])
        root.attrib['expected_failures'] = str(data['expected_failures'])
        root.attrib['unexpected_success'] = str(data['unexpected_success'])
        for test_case in data['test_cases']:
            name_details = test_case.split(".")
            name = name_details[-1]
            class_name = ".".join(name_details[0:-1:1])

            test_case_element = SubElement(
                    root,
                    test_case_tag,
                    {
                        time_attribute:
                            str(data['test_cases'][test_case][time_attribute]),
                        name_attribute:
                            name,
                        class_name_attribute:
                            class_name
                    }
            )
            status = str(data['test_cases'][test_case][status_attribute])
            if status != success_status:
                if status == skip_status:
                    tag_to_add = skip_tag
                    status_element = SubElement(
                        test_case_element,
                        tag_to_add
                    )
                else:
                    tag_to_add = fail_tag if status == fail_status \
                        else error_tag
                    message = \
                        str(data['test_cases'][test_case][traceback_attribute])
                    status_element = SubElement(
                        test_case_element,
                        tag_to_add,
                        {
                            message_attribute: failed_test_message,
                        },
                    )
                    status_element.text = message

        with open("verification.xml", "w") as output_file:
            output_file.write(prettify(root))
