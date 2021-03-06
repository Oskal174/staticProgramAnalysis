class functional_object:
    def __init__(self, code, symbol, location, id):
        self.code = code
        self.symbol = symbol
        self.location = location
        self.id = id

    def get_id(self):
        return self.id

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def get_symbol_spaces(self):
        return ' ' + self.symbol + ' '

    def get_code(self):
        return self.code
    
    def get_location(self):
        return self.location

    def __str__(self):
        return self.get_id() + " : " + self.get_location() + " : " + self.get_code() + ' -> ' + self.get_symbol()

    # for write to file
    def get_str(self):
        return self.get_id() + " : " + self.get_location() + " : " + self.get_code() + ' -> ' + self.get_symbol() + '\n'
