


class EcoStressDataset:

    def __init__(self, path):
        self.path = path
        self.dataset = None
        self.load()
