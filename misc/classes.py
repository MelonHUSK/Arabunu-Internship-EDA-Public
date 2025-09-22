class Band:
    def __init__(self, name, vocalist, guitarist):
        self.name = name
        self.vocalist = vocalist
        self.guitarist = guitarist

    def bandInfo(self):
        print("The band " + self.name + " is composed of vocalist " + self.vocalist + " and guitarist " + self.guitarist + ".")

band1 = Band("BMTH", "Oli Sykes", "Lee Malia")
band1.bandInfo()