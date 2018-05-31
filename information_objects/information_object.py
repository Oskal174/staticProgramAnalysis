class information_object:
    def __init__(self, code, symbol, location, id):
        self.code = code
        self.symbol = symbol
        self.location = location
        self.id = id

    def get_id(self):
        return self.id

    def get_code(self):
        return self.code
    
    def get_location(self):
        return self.location

    def __str__(self):
        return self.get_id() + " : " + self.get_location() + " : " + self.get_code()