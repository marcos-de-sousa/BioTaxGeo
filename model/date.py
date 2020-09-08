class Date:

    def __init__(self, date=None):
        self.separator = [".", "-", "/"]
        self.date = date or ""
        self.new_date = {"date": date, "day": False, "month": False, "year": False}

    def set_Date(self, date):
        self.date = date

    def get_Date(self):
        return self.date

    def is_Have_Separator(self, date):
        for s in self.separator:
            if s in date:
                return True
        return False

    def get_Date_Separator(self, date):
        for s in date:
            if s in self.separator:
                return s
        return None
    def set_New_Date(self, day, month, year, date):
        self.new_date = {"date": date, "day": day, "month": month, "year": year}

    def get_New_Date(self):
        return self.new_date

    def toDDMMAAAA(self, date, type_separator, init_format):
        if(self.is_Have_Separator(date)):
            separator = self.get_Date_Separator(date)
            split_date = date.split(separator)
            if init_format == "DDMMAAAA":
                day = self.checkDay(split_date[0])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[0]}{type_separator}{split_date[1]}{type_separator}{split_date[2]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "MMDDAAAA":
                day = self.checkDay(split_date[1])
                month = self.checkMonth(split_date[0])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[1]}{type_separator}{split_date[0]}{type_separator}{split_date[2]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "AAAAMMDD":
                day = self.checkDay(split_date[2])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[0])
                date_formated = f"{split_date[2]}{type_separator}{split_date[1]}{type_separator}{split_date[0]}"
                self.set_New_Date(day, month, year, date_formated)
            return self.get_New_Date()
        else:
            self.set_New_Date(date=date)
            return self.get_New_Date()
        return "Error"

    def toMMDDAAAA(self, date, type_separator, init_format):
        if(self.is_Have_Separator(date)):
            separator = self.get_Date_Separator(date)
            split_date = date.split(separator)
            if init_format == "DDMMAAAA":
                day = self.checkDay(split_date[0])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[1]}{type_separator}{split_date[0]}{type_separator}{split_date[2]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "MMDDAAAA":
                day = self.checkDay(split_date[1])
                month = self.checkMonth(split_date[0])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[0]}{type_separator}{split_date[1]}{type_separator}{split_date[2]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "AAAAMMDD":
                day = self.checkDay(split_date[2])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[0])
                date_formated = f"{split_date[1]}{type_separator}{split_date[2]}{type_separator}{split_date[0]}"
                self.set_New_Date(day, month, year, date_formated)
            return self.get_New_Date()
        else:
            self.set_New_Date(date=date)
            return self.get_New_Date()
        return "Error"

    def toAAAAMMDD(self, date, type_separator, init_format):
        if(self.is_Have_Separator(date)):
            separator = self.get_Date_Separator(date)
            split_date = date.split(separator)
            if init_format == "DDMMAAAA":
                day = self.checkDay(split_date[0])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[2]}{type_separator}{split_date[1]}{type_separator}{split_date[0]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "MMDDAAAA":
                day = self.checkDay(split_date[1])
                month = self.checkMonth(split_date[0])
                year = self.checkYear(split_date[2])
                date_formated = f"{split_date[2]}{type_separator}{split_date[0]}{type_separator}{split_date[1]}"
                self.set_New_Date(day, month, year, date_formated)
            if init_format == "AAAAMMDD":
                day = self.checkDay(split_date[2])
                month = self.checkMonth(split_date[1])
                year = self.checkYear(split_date[0])
                date_formated = f"{split_date[2]}{type_separator}{split_date[1]}{type_separator}{split_date[0]}"
                self.set_New_Date(day, month, year, date_formated)
            return self.get_New_Date()
        else:
            self.set_New_Date(date=date)
            return self.get_New_Date()
        return "Error"

    def checkDay(self, day):
        new_day = int(day)
        if new_day > 0 and new_day < 31:
            return False
        else:
            return True
        return day

    def checkMonth(self, month):
        new_month = int(month)
        if new_month > 0 and new_month < 13:
            return False
        else:
            return True
        return day

    def checkYear(self, year):
        return not year.isdigit()