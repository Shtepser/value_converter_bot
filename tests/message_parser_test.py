import unittest

from converter_bot.message_parser import MessageParser


class MessageParserTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = MessageParser()

    def test_simple_measures(self):
        cases = [("грамм", "gram"), ("стаканов", "beaker"), ("нечто", None)]
        for case, correct in cases:
            answer = self.parser.parse_measure(case)
            self.assertEqual(answer, correct)

    def test_complex_measures(self):
        cases = [("чайных ложек", "teaspoon"), ("столовых ложек", "tablespoon"),
                 ("ложек", None), ("чайных вещей", None)]
        for case, correct in cases:
            answer = self.parser.parse_measure(case)
            self.assertEqual(answer, correct)

    def test_simple_substances(self):
        cases = [("муки", "flour"), ("воды", "water"), ("нечто", None)]
        for case, correct in cases:
            answer = self.parser.parse_substance(case)
            self.assertEqual(answer, correct)

    def test_complex_substances(self):
        cases = [("оливкового масла", "olive_oil"), ("сливочного масла", "butter"),
                 ("оливкового нечта", None), ("оливкового", None)]
        for case, correct in cases:
            answer = self.parser.parse_substance(case)
            self.assertEqual(answer, correct)

    def test_simple_messages(self):
        cases = [("12 граммов муки > стаканы", (12.0, 'gram', 'flour', 'beaker')),
                 ("0,5 килограмма муки > стаканы", (0.5, 'kilogram', 'flour', 'beaker'))]
        for case, correct in cases:
            answer = self.parser.parse(case)
            self.assertTupleEqual(answer, correct)

    def test_complex_messages(self):
        cases = [("12 граммов оливкового масла > чайные ложки", (12.0, 'gram', 'olive_oil',
                                                                 'teaspoon')),
                 ("3 столовые ложки сливочного масла > чайные ложки", (3, 'tablespoon', 'butter',
                                                                       'teaspoon'))]
        for case, correct in cases:
            answer = self.parser.parse(case)
            self.assertTupleEqual(answer, correct)


if __name__ == '__main__':
    unittest.main()
