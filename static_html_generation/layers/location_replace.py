import re

class LocationReplace(object):
    """ Applies location based layers to XML nodes. """
    def __init__(self):
        self.counter = 0
        self.offset_starter = 0
        self.offset_counters = None
        self.offsets = None

    @staticmethod
    def find_all_offsets(pattern, text):
        return [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), text)]

    @staticmethod
    def replace_at_offset(offset, replacement, text):
        return text[:offset[0]] + replacement + text[offset[1]:]

    def update_offsets(self, original, text):
        list_offsets = LocationReplace.find_all_offsets(original, text)
        self.offset_counters = range(self.offset_starter, self.offset_starter + len(list_offsets))
        self.offsets = {c:pair for (c, pair) in list(zip(self.offset_counters, list_offsets))}

    def update_offset_starter(self):
        if len(self.offset_counters) > 0:
            self.offset_starter =self.offset_counters[-1] + 1

    def apply_layer_to_text(self, original, replacement, text, locations):
        self.update_offsets(original, text)
        offset = self.offsets[locations[self.counter]]

        self.counter += 1
        return LocationReplace.replace_at_offset(offset, replacement, text)

    def location_replace(self, xml_node, original, replacement, locations):
        """ For the xml_node, replace the locations instances of orginal with replacement."""
        if xml_node.text:
            self.update_offsets(original, xml_node.text)

            while self.counter < len(locations) and locations[self.counter] in self.offsets:
                xml_node.text = self.apply_layer_to_text(original, replacement, xml_node.text, locations)

            self.update_offset_starter()

        for c in xml_node.getchildren():
            self.location_replace(c, original, replacement, locations)

        if xml_node.tail:
            self.update_offsets(original, xml_node.tail)

            while self.counter < len(locations) and locations[self.counter] in self.offsets:
                xml_node.tail = self.apply_layer_to_text(original, replacement, xml_node.tail, locations)
            self.update_offset_starter()
