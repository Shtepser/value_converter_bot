from itertools import chain


class Measurements:

    def __init__(self):
        self.masses = {'tonne': 1000, 'kilogram': 1, 'gram': 0.001}
        self.base_mass = 'kilogram'
        self.volumes = {'cubic_metre': 1, 'litre': 0.001, 'beaker': 0.000250,
                        'millilitre': 0.000001, 'tablespoon': 0.000018, 'teaspoon': 0.000005}
        self.base_volume = 'cubic_metre'
        self.densities = {'olive_oil': 920, 'water': 1000, 'milk': 1040,
                          'butter': 920, 'sugar': 720, 'flour': 1430}
        self.translations = {'ru': {
            "tonne": "тонна",
            "kilogram": "килограмм",
            "gram": "грамм",
            "cubic_metre": "кубический метр",
            "litre": "литр",
            "millilitre": "миллилитр",
            "teaspoon": "чайная ложка",
            "tablespoon": "столовая ложка",
            "beaker": "стакан",
            "olive_oil": "оливковое масло",
            "water": "вода",
            "milk": "молоко",
            "butter": "сливочное масло",
            "sugar": "сахар",
            "flour": "мука"
        }}

    def get_measurements(self, lang):
        measures = chain(self.masses, self.volumes)
        dictionary = self.translations[lang]
        return {dictionary[measure]: measure if measure in dictionary else (measure, measure)
                for measure in measures}

    def get_substances(self, lang):
        dictionary = self.translations[lang]
        return {dictionary[subst]: subst if subst in dictionary else (subst, subst)
                for subst in self.densities}

    def get_measurements_at_lang(self, lang):
        measures = chain(self.masses, self.volumes)
        dictionary = self.translations[lang]
        return {measure: dictionary[measure] if measure in dictionary else (measure, measure)
                for measure in measures}

    def get_substances_at_lang(self, lang):
        dictionary = self.translations[lang]
        return {subst: dictionary[subst] if subst in dictionary else (subst, subst)
                for subst in self.densities.keys()}