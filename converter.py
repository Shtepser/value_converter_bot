class MassVolumeConverter:

    def __init__(self, measurement_system):
        self.measurements = measurement_system

    def convert(self, substance, original, requested, quantity):
        """ Converts substance quantity in original unit into requirement unit """
        if original in self.measurements.masses:
            if requested in self.measurements.masses:
                return self.convert_masses(original, requested, quantity)
            return self.convert_mass_to_volume(substance, original, requested, quantity)
        if requested in self.measurements.masses:
            return self.convert_volumes(original, requested, quantity)
        return self.convert_volume_to_mass(substance, original, requested, quantity)

    def convert_mass_to_volume(self, substance, original, requested, quantity):
        volume = self.measurements.masses[original] / self.measurements.densities[substance] * \
                 quantity
        return self.convert_volumes(self.measurements.base_volume, requested, volume)

    def convert_volume_to_mass(self, substance, original, requested, quantity):
        mass = self.measurements.volumes[original] * self.measurements.densities[substance] * \
                quantity
        return self.convert_masses(self.measurements.base_mass, requested, mass)

    def convert_masses(self, original, requested, quantity):
        return self.measurements.masses[original] / self.measurements.masses[requested] * quantity

    def convert_volumes(self, original, requested, quantity):
        return self.measurements.volumes[original] / self.measurements.volumes[requested] * quantity
