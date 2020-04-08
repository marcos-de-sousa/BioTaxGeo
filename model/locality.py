class Locality:

    def __init__(self, sht):
        self.country = []
        self.state = []
        self.county = []
        self.local = []
        self.sheet = sht

    def set_Country_Column_values(self, country):
        if (type(country) == str):
            index_column = self.sheet.row_values(0).index(country)
            self.country = self.sheet.col_values(index_column, 1)
        elif (type(country) == int):
            self.country = self.sheet.col_values(country, 1)
        elif (type(country) == dict):
            self.country = country

    def set_State_Column_values(self, state):
        if (type(state) == str):
            index_column = self.sheet.row_values(0).index(state)
            self.state = self.sheet.col_values(index_column, 1)
        elif (type(state) == int):
            self.state = self.sheet.col_values(state, 1)
        elif (type(state) == dict):
            self.state = state

    def set_County_Column_values(self, county):
        if (type(county) == str):
            index_column = self.sheet.row_values(0).index(county)
            self.county = self.sheet.col_values(index_column, 1)
        elif (type(county) == int):
            self.county = self.sheet.col_values(county, 1)
        elif (type(county) == dict):
            self.county = county

    def set_Local_Column_values(self, local):
        if (type(local) == str):
            index_column = self.sheet.row_values(0).index(local)
            self.local = self.sheet.col_values(index_column, 1)
        elif (type(local) == int):
            self.local = self.sheet.col_values(local, 1)
        elif (type(local) == dict):
            self.local = local


    def get_Country_Column_values(self):
        if (self.country == []):
            return "Empty column."
        else:
            return self.country

    def get_State_Column_values(self):
        if (self.state == []):
            return "Empty column."
        else:
            return self.state
        
    def get_County_Column_values(self):
        if (self.county == []):
            return "Empty column."
        else:
            return self.county

    def get_Local_Column_values(self):
        if (self.local == []):
            return "Empty column."
        else:
            return self.local
