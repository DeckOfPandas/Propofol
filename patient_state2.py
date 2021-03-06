class PatientState2:
    # age: years
    # weight: kilos
    # height: cm
    # sex: 'm' or 'f'
    def __init__(self, age, weight, height, sex, params):
        self.params = params

        lean_body_mass = self.__lean_body_mass(weight, height, sex)

        self.v1 = (params['v1a'] - params['v1b']*(age - params['age_offset'])) * (params['v1c'] * (lean_body_mass - params['lbm_offset']))
        self.v2 = params['v2a'] * lean_body_mass
        self.v3 = params['v3a'] * weight

        # Initial concentration is zero in all components
        self.x1 = 0.0
        self.x2 = 0.0
        self.x3 = 0.0

        self.k10 = (params['k10a'] * self.v1) / 60
        self.k12 = params['k12'] /60
        self.k13 = params['k13'] / 60
        self.k21 = (params['k12'] * (self.v1/self.v2)) / 60
        self.k31 = (params['k13'] * (self.v1/self.v3)) / 60

        self.keo = 0.456 / 60

        self.xeo = 0.0

    def give_drug(self, drug_milligrams):
        self.x1 = self.x1 + drug_milligrams / self.v1

    def wait_time(self, time_seconds):

        x1k10 = self.x1 * self.k10
        x1k12 = self.x1 * self.k12
        x1k13 = self.x1 * self.k13
        x2k21 = self.x2 * self.k21
        x3k31 = self.x3 * self.k31

        self.x1 = self.x1 + (x2k21 - x1k12 + x3k31 - x1k13 - x1k10) * time_seconds
        self.x2 = self.x2 + (x1k12 - x2k21) * time_seconds
        self.x3 = self.x3 + (x1k13 - x3k31) * time_seconds
    @staticmethod
    def with_schnider_params(age, weight, height, sex):
        params = PatientState.schnider_params()

        return PatientState(age, weight, height, sex, params)

    @staticmethod
    def schnider_params():
        params = {
            'k10a': 0.443,
            'k10b': 0.0107,
            'k10c': -0.0159,
            'k10d': 0.0062,
            'k12a': 0.302,
            'k12b': -0.0056,
            'k13': 0.196,
            'k21a': 1.29,
            'k21b': -0.024,
            'k21c': 18.9,
            'k21d': -0.391,
            'k31': 0.0035,
            'v1': 4.27,
            'v3': 238,
            'age_offset': 53,
            'weight_offset': 77,
            'lbm_offset': 59,
            'height_offset': 177
        }
        return params

    def __lean_body_mass(self, weight, height, sex):
        if sex != "m" and sex != "f":
            raise ValueError("Unknown sex '%s'. This algorithm can only handle 'm' and 'f'. :(" % sex)

        if sex == "m":
            return (0.32819 * weight) + (0.33929 * height) - 29.5336
        else:
            return (0.29569 * weight) + (0.41813 * height) - 43.2933

    def __repr__(self):
        return "PatientState(x1=%f, x2=%f, x3=%f, xeo=%f)" % (self.x1, self.x2, self.x3, self.xeo)


if __name__ == '__main__':
    patient = PatientState.with_schnider_params(50, 70, 180, "m")
    print "Initial state: " + str(patient)

    patient.give_drug(92.60001)
    print "After giving drug: " + str(patient)

    for t in range(130):
        patient.wait_time(1)
        print "After 1 sec: " + str(patient)
