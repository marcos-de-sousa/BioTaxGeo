class Date:

    def __init__(self, date=None):
        self.separator = [".", "-", "/"]
        self.date = date or ""

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

    def toDDMMAAAA(self, date, type_separator, init_format):
        new_date = {"date": date, "day": False, "month": False}
        if(self.is_Have_Separator(date)):
            separator = self.get_Date_Separator(date)
            split_date = date.split(separator)

            if init_format == "DDMMAAAA":
                new_date["day"] = self.checkDay(split_date[0])
                new_date["month"] = self.checkMonth(split_date[1])
                new_date["date"] = f"{split_date[0]}{type_separator}{split_date[1]}{type_separator}{split_date[2]}"
            if init_format == "MMDDAAAA":
                new_date["day"] = self.checkDay(split_date[1])
                new_date["month"] = self.checkMonth(split_date[0])
                new_date["date"] = f"{split_date[1]}{type_separator}{split_date[0]}{type_separator}{split_date[2]}"
            return new_date
        else:
            return new_date
        return "Error"

    def toMMDDAAAA(self, date, type_separator, init_format):
        new_date = {"date": date, "day": False, "month": False}
        if(self.is_Have_Separator(date)):
            separator = self.get_Date_Separator(date)
            split_date = date.split(separator)
            if init_format == "DDMMAAAA":
                new_date["day"] = self.checkDay(split_date[0])
                new_date["month"] = self.checkMonth(split_date[1])
                new_date["date"] = f"{split_date[1]}{type_separator}{split_date[0]}{type_separator}{split_date[2]}"
            if init_format == "MMDDAAAA":
                new_date["day"] = self.checkDay(split_date[1])
                new_date["month"] = self.checkMonth(split_date[0])
                new_date["date"] = f"{split_date[0]}{type_separator}{split_date[1]}{type_separator}{split_date[2]}"
            return new_date
        else:
            return new_date
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