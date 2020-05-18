class MassVolumeConverter:
    MASSES = {'tonne': 1000, 'kilogram': 1, 'gram': 0.001}
    VOLUMES = {'cubic_metre': 1, 'litre': 0.001, 'millilitre': 0.000001, 'teaspoon': 0.000005}
    DENSITIES = {'olive_oil': 920, 'water': 1000, 'milk': 1040, 'butter': 920, 'sugar': 720}

    def convert(self, substance, original, requested, quantity):
        """ Converts substance quantity in original unit into requirement unit """
        if original in self.MASSES:
            if requested in self.MASSES:
                return self.convert_masses(original, requested, quantity)
            return self.convert_mass_to_volume(substance, original, requested, quantity)
        if requested in self.MASSES:
            return self.convert_volumes(original, requested, quantity)
        return self.convert_volume_to_mass(substance, original, requested, quantity)

    def convert_mass_to_volume(self, substance, original, requested, quantity):
        volume_in_cubic_metres = self.MASSES[original] / self.DENSITIES[substance] * quantity
        return self.convert_volumes('cubic_metre', requested, volume_in_cubic_metres)

    def convert_volume_to_mass(self, substance, original, requested, quantity):
        mass_in_kilograms = self.VOLUMES[original] * self.DENSITIES[substance] * quantity
        return self.convert_masses('kilogram', requested, mass_in_kilograms)

    def convert_masses(self, original, requested, quantity):
        return self.MASSES[original] / self.MASSES[requested] * quantity

    def convert_volumes(self, original, requested, quantity):
        return self.VOLUMES[original] / self.VOLUMES[requested] * quantity
