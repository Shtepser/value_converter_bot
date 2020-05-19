from pymorphy2 import MorphAnalyzer
from converter_bot.measurements import Measurements


class MessageParser:

    def __init__(self, lang='ru'):
        self.lang = lang
        measurements = Measurements()
        self.measurements = measurements.get_measurements(lang)
        self.substances = measurements.get_substances(lang)
        self.morph = MorphAnalyzer()

    @property
    def correct_measurements(self):
        return self.measurements.keys()

    @property
    def correct_substances(self):
        return self.substances.keys()

    def parse(self, message: str) -> (float, str, str, str):
        """
        parses raw message

        :param message: message to parse (scheme: quantity measure substance > target measure)
        :return: quantity(float), base_measure, substance, target_measure
        """
        left, right = message.strip().split(" > ")
        quantity, *start_measure_and_substance = left.split(' ')
        quantity = self.__parse_quantity(quantity)
        base_measure, substance = self.__parse_measure_and_substance(start_measure_and_substance)
        target_measure = self.parse_measure(right)
        res = quantity, base_measure, substance, target_measure
        if any(elem is None for elem in res):
            return None
        return res

    def parse_measure(self, measure: str):
        """
        parses measure

        :param measure: string to parse
        :return: measure or None (if measure can't be parsed
        """
        words = measure.split()
        if len(words) == 1:
            potential_measure = self.morph.parse(measure)[0].normalized.word
        elif len(words) == 2:
            noun = self.morph.parse(words[1])[0]
            adjective = self.morph.parse(words[0])[0]
            try:
                potential_measure = self.__construct_normal_form_word_pair(noun, adjective)
            except ValueError:
                return None
        else:
            return None
        if potential_measure in self.correct_measurements:
            return self.measurements[potential_measure]
        return None

    def parse_substance(self, substance: str):
        """
        parses substance

        :param substance: string to parse
        :return: substance or None (if measure can't be parsed
        """
        words = substance.split()
        if len(words) == 1:
            potential_substance = self.morph.parse(substance)[0].normalized.word
        else:
            noun = self.morph.parse(words[1])[0]
            adjective = self.morph.parse(words[0])[0]
            try:
                potential_substance = self.__construct_normal_form_word_pair(noun, adjective)
            except ValueError:
                return None
        if potential_substance in self.correct_substances:
            return self.substances[potential_substance]
        return None

    @staticmethod
    def __construct_normal_form_word_pair(noun, adjective):
        noun = noun.normalized
        adj = adjective.normalized.inflect({noun.tag.gender})
        return adj.word + ' ' + noun.word

    def __parse_quantity(self, quantity):
        if self.lang == 'ru':
            quantity = quantity.replace(',', '.')
        try:
            return float(quantity)
        except ValueError:
            return None

    def __parse_measure_and_substance(self, words):
        for i in range(1, len(words)):
            measure = self.parse_measure(' '.join(words[:i]))
            if measure:
                substance = self.parse_substance(' '.join(words[i:]))
                if substance:
                    return measure, substance
