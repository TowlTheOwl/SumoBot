class Database:
    def __init__(self, id):
        self.data = ['10', '10', '10', '10', '10', '10']
        self.id = id

    def get_data(self):
        return self.data

    def input_data(self, data):
        self.data = data.strip("[]").replace("'", "").split(', ')
