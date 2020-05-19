import unittest

from converter_bot.converter import MassVolumeConverter
from converter_bot.measurements import Measurements


class MassVolumeConverterTest(unittest.TestCase):

    def setUp(self):
        self.converter = MassVolumeConverter(Measurements())

    def test_masses(self):
        cases = [('kilogram', 'tonne', 32, 0.032), ('tonne', 'gram', 2.16, 2160000)]
        for orig, req, quantity, correct in cases:
            answer = self.converter.convert_masses(orig, req, quantity)
            self.assertAlmostEqual(answer, correct, places=3)

    def test_volumes(self):
        cases = [('millilitre', 'teaspoon', 5, 1), ('millilitre', 'cubic_metre', 10000, 0.01)]
        for orig, req, quantity, correct in cases:
            answer = self.converter.convert_volumes(orig, req, quantity)
            self.assertAlmostEqual(answer, correct, places=3)

    def test_convert_mass_to_volume(self):
        cases = [('olive_oil', 'kilogram', 'cubic_metre', 920, 1),
                 ('sugar', 'gram', 'teaspoon', 25, 6.9444)]
        for subst, orig, req, quantity, correct in cases:
            answer = self.converter.convert_mass_to_volume(subst, orig, req, quantity)
            self.assertAlmostEqual(answer, correct, places=3)

    def test_convert_volume_to_mass(self):
        cases = [('olive_oil', 'cubic_metre', 'kilogram', 1, 920),
                 ('sugar', 'teaspoon', 'gram', 6.9444, 25)]
        for subst, orig, req, quantity, correct in cases:
            answer = self.converter.convert_volume_to_mass(subst, orig, req, quantity)
            self.assertAlmostEqual(answer, correct, places=3)


if __name__ == '__main__':
    unittest.main()
