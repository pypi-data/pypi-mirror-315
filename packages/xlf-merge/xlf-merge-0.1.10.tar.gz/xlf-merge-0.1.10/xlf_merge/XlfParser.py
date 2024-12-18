from lxml import etree, html
import re
from typing import List


# Regex to strip starting and ending XML tags of a byte string
re_xml_open_close = re.compile(rb'^<[^>]+>|</[^>]+>$')


class XlfParser:
    trans_units = []
    nsmap = None

    def __init__(self, trans_units: List[dict], root: etree.Element, nsmap: dict):
        self.trans_units = trans_units
        self.root = root
        self.nsmap = nsmap

    @staticmethod
    def from_xml(xls_content: str | bytes) -> 'XlfParser':
        root = XlfParser.parse_xml(xls_content)
        nsmap = root.nsmap

        file = root.find('file', nsmap)
        body = file.find('body', nsmap)
        trans_units = []
        trans_units_elements = body.findall('trans-unit', nsmap)
        for trans_units_element in trans_units_elements:

            source = trans_units_element.find('source', nsmap)
            source_text = re_xml_open_close.sub(b'', etree.tostring(source))
            target = trans_units_element.find('target', nsmap)
            if target is not None:
                target_text = re_xml_open_close.sub(b'', etree.tostring(target))
            else:
                target_text = ''

            context_groups = []
            context_group_elements = trans_units_element.findall('context-group', nsmap)
            for context_group_element in context_group_elements:
                contexts = []
                for context_element in context_group_element.findall('context', nsmap):
                    contexts.append({
                        'attrib': context_element.attrib,
                        'text': context_element.text
                    })

                context_groups.append({
                    'attrib': context_group_element.attrib,
                    'contexts': contexts
                })

            data = {
                'attrib': trans_units_element.attrib,
                'source': {
                    'text': source_text,
                    'attrib': source.attrib
                },
                'context-groups': context_groups
            }

            if target is not None:
                data['target'] = {
                    'text': target_text,
                    'attrib': target.attrib
                }

            trans_units.append(data)

        return XlfParser(trans_units, root, nsmap)

    @staticmethod
    def from_trans_units(trans_units: List[dict], target_language: str | None = None) -> 'XlfParser':
        nsmap = {None: 'urn:oasis:names:tc:xliff:document:1.2'}
        root = etree.Element('xliff', nsmap=nsmap)
        root.set('version', '1.2')

        file = etree.Element('file', nsmap=nsmap)
        file.set('source-language', 'en')
        if target_language:
            file.set('target-language', target_language)
        file.set('datatype', 'plaintext')
        file.set('original', 'ng2.template')

        body = etree.Element('body', nsmap=nsmap)

        file.append(body)

        root.append(file)

        xml: bytes = XlfParser.generate_xml(root)

        return XlfParser(trans_units, XlfParser.parse_xml(xml), nsmap)

    def get_trans_units(self):
        return self.trans_units

    def set_trans_units(self, trans_units: List[str]):
        self.trans_units = trans_units

    def append_mixed(self, content_tag: etree.Element, mixed: str):
        for elem in html.fragments_fromstring(mixed):
            if type(elem) == str:
                content_tag.text = elem
            else:
                content_tag.append(elem)

    def get_target_language(self):
        return self.root.find('file', self.nsmap).get('target-language')

    def to_xml(self) -> bytes:
        file = self.root.find('file', self.nsmap)
        body = file.find('body', self.nsmap)
        body.clear()
        for trans_unit in self.trans_units:
            trans_unit_element = etree.Element('trans-unit', attrib=trans_unit['attrib'], nsmap=self.nsmap)

            source_element = etree.Element('source', attrib=trans_unit['source']['attrib'], nsmap=self.nsmap)
            self.append_mixed(source_element, trans_unit['source']['text'])
            trans_unit_element.append(source_element)

            for context_group in trans_unit.get('context-groups'):
                context_group_element = etree.Element('context-group', attrib=context_group['attrib'], nsmap=self.nsmap)

                for context in context_group['contexts']:
                    context_element = etree.Element('context', attrib=context['attrib'], nsmap=self.nsmap)
                    context_element.text = context['text']

                    context_group_element.append(context_element)

                trans_unit_element.append(context_group_element)

            found_target = trans_unit.get('target')
            if found_target:
                target_element = etree.Element('target', attrib=found_target['attrib'], nsmap=self.nsmap)
                self.append_mixed(target_element, found_target['text'])
                trans_unit_element.append(target_element)

            body.append(trans_unit_element)

        return XlfParser.generate_xml(self.root)

    @staticmethod
    def parse_xml(xml: str | bytes) -> etree.Element:
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        if not isinstance(xml, bytes):
            xml = xml.encode('UTF-8')
        el = etree.ElementTree(etree.fromstring(xml, parser))
        return el.getroot()

    @staticmethod
    def generate_xml(root: etree.Element) -> bytes:
        return etree.tostring(root, encoding='utf8', method='xml', pretty_print=True, xml_declaration=True)
