class Data:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.data = []

    def get_data(self):
        return self.data

    def input_data(self, data):
        self.data = data

    def connected(self):
        return self.ready