class Coordinate:

    def __init__(self, sht):
        self.latitude_column = []
        self.longitude_column = []
        self.index_row_lat = []
        self.index_row_lng = []
        self.sheet = sht
        self.coordinate = {
            "latitude":
                {
                    "degree": None,
                    "minute": None,
                    "second": None,
                    "hemisphere": None,
                    "decimal": None
                },
            "longitude":
                {
                    "degree": None,
                    "minute": None,
                    "second": None,
                    "hemisphere": None,
                    "decimal": None
                }
        }
        self.coordinate_list = []
        self.hemisphere = ["w", "W", "s", "S", "e", "E", "n", "N"]

    def set_Latitude_Column_values(self, lat_column):
        if (type(lat_column) == str):
            index_column = self.sheet.row_values(0).index(lat_column)
            count = 2
            self.latitude_column = self.sheet.col_values(index_column, 1)
            for row in self.latitude_column:
                if(row!=""):
                    self.index_row_lat.append(count)
                count += 1
        elif (type(lat_column) == int):
            self.latitude_column = self.sheet.col_values(lat_column, 1)
        elif (type(lat_column) == dict):
            self.latitude_column = lat_column

    def set_Longitude_Column_values(self, lng_column):
        if (type(lng_column) == str):
            index_column = self.sheet.row_values(0).index(lng_column)
            count=2
            self.longitude_column = self.sheet.col_values(index_column, 1)
            for row in self.longitude_column:
                if(row!=""):
                    self.index_row_lng.append(count)
                count += 1
        elif (type(lng_column) == int):
            self.longitude_column = self.sheet.col_values(lng_column, 1)
        elif (type(lng_column) == dict):
            self.longitude_column = lng_column

    def get_Latitude_Column_values(self):
        if (self.latitude_column == []):
            return "Empty column."
        else:
            return self.latitude_column

    def get_Longitude_Column_values(self):
        if (self.longitude_column == []):
            return "Empty column."
        else:
            return self.longitude_column
    
    def get_Index_Row_Lat(self):
        if (self.index_row_lat == []):
            return "Empty array."
        else:
            return self.index_row_lat

    def get_Index_Row_Lng(self):
        if (self.index_row_lng == []):
            return "Empty array."
        else:
            return self.index_row_lng

    # Precisa ser melhorado o método que os valores são inseridos no dicionario coordinates. Mas por enquanto vai ser feito assim.
    def Format_Lat_Lng (self, coord, coord_name):  # Bem vindo a loucura de Elielson. Ta grande, mas funciona.
        split_value = str(coord).split()
        join_value = " ".join(split_value)
        spaces = join_value.count(" ")
        last_hemisphere = False
        negative_hemisphere = ["w", "W", "s", "S"]
        have_hemisph = True if list(set(self.hemisphere).intersection(split_value)) != [] else False
        emisf_neg = True if list(set(split_value).intersection(negative_hemisphere)) != [] else False
        # Caso a coordinate tenha alguma letra, significa que o decimal dela será descrito como positivo ou negativo com base no emisfério descrito
        if have_hemisph:
            for coordinate in split_value:
                # Caso a coordinate esteja em formato degree, minute por second.
                if spaces == 3:

                    # Referente ao emisfério
                    if (coordinate in self.hemisphere) and (split_value.index(coordinate) != 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate
                        if (emisf_neg):
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1
                    elif (coordinate in self.hemisphere) and (split_value.index(coordinate) == 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate

                    # Referente ao degree
                    if ("°" in coordinate) or ("º" in coordinate):
                        if split_value.index(coordinate) == 0:
                            last_hemisphere = True
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-", "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif (coordinate not in self.hemisphere) and (split_value.index(coordinate) == 0):
                        last_hemisphere = True
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-", "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 1) and last_hemisphere == False:
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        if emisf_neg:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1

                    # Referente aos minutes
                    if ("'" in coordinate):
                        self.coordinate[coord_name]["minute"] = coordinate.replace("'", "").replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 1) and last_hemisphere:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["minute"]:
                            self.coordinate[coord_name]["minute"] = self.coordinate[coord_name]["minute"].replace("-",
                                                                                                                    "")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 2) and last_hemisphere == False:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                        if emisf_neg:
                            self.coordinate[coord_name]["minute"] = self.coordinate[coord_name]["minute"] * -1

                    # Referente aos seconds
                    if ('"' in coordinate):
                        self.coordinate[coord_name]["second"] = coordinate.replace('"', "").replace(",", ".")
                        self.coordinate[coord_name]["second"] = float(self.coordinate[coord_name]["second"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 2) and last_hemisphere:
                        self.coordinate[coord_name]["second"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["second"]:
                            self.coordinate[coord_name]["second"] = self.coordinate[coord_name]["second"].replace(
                                "-", "")
                        self.coordinate[coord_name]["second"] = float(self.coordinate[coord_name]["second"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 3) and last_hemisphere == False:
                        self.coordinate[coord_name]["second"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["second"] = float(self.coordinate[coord_name]["second"])
                        if emisf_neg:
                            self.coordinate[coord_name]["second"] = self.coordinate[coord_name]["second"] * -1

                # Caso a coordinate esteja em formato degree por minute.
                if spaces == 2:

                    # Referente ao emisfério
                    if (coordinate in self.hemisphere) and (split_value.index(coordinate) != 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate.replace(",", ".")
                        if (emisf_neg):
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1
                    elif (coordinate in self.hemisphere) and (split_value.index(coordinate) == 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate.replace(",", ".")

                    # Referente ao degree
                    if ("°" in coordinate) or ("º" in coordinate):
                        if (split_value.index(coordinate) == 0):
                            last_hemisphere = True
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-", "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif (coordinate not in self.hemisphere) and (split_value.index(coordinate) == 0):
                        last_hemisphere = True
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-", "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 1) and last_hemisphere == False:
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        if emisf_neg:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1

                    # Referente ao minute
                    if "'" in coordinate:
                        self.coordinate[coord_name]["minute"] = coordinate.replace("'", "").replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 1) and last_hemisphere:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["minute"]:
                            self.coordinate[coord_name]["minute"] = self.coordinate[coord_name]["minute"].replace("-",
                                                                                                                    "")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif (coordinate not in self.hemisphere) and (
                            split_value.index(coordinate) == 2) and last_hemisphere == False:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                        if emisf_neg:
                            self.coordinate[coord_name]["minute"] = self.coordinate[coord_name]["minute"] * -1

                            # Caso a coordinate esteja em degree/Decimal somente
                if spaces == 1:

                    # Referente ao emisfério
                    if (coordinate in self.hemisphere) and (split_value.index(coordinate) != 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate.replace(",", ".")
                        if (emisf_neg):
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1
                            self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]
                    elif (coordinate in self.hemisphere) and (split_value.index(coordinate) == 0):
                        self.coordinate[coord_name]["hemisphere"] = coordinate.replace(",", ".")

                    # Referente ao degree
                    if ("°" in coordinate) or ("º" in coordinate):
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-",
                                                                                                                "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]
                    elif (coordinate not in self.hemisphere) and (split_value.index(coordinate) == 0):
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        if "-" in self.coordinate[coord_name]["degree"]:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"].replace("-", "")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]
                    elif (coordinate not in self.hemisphere) and (split_value.index(coordinate) == 1):
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        if emisf_neg:
                            self.coordinate[coord_name]["degree"] = self.coordinate[coord_name]["degree"] * -1
                        self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]
        # Caso não tenha nenhuma letra, o emisfério e descrito apenas pelo sinal de '-', se for positivo é norte, se for negativo é sul.
        else:

            for coordinate in split_value:

                # Caso a coordinate esteja em formato degree, minute por second.
                if spaces == 2:

                    # Referente ao degree.
                    if ("°" in coordinate) or ("º" in coordinate):
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif split_value.index(coordinate) == 0:
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])

                    # Referente ao minute
                    if "'" in coordinate:
                        self.coordinate[coord_name]["minute"] = coordinate.replace("'", "").replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif split_value.index(coordinate) == 1:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])

                    # Referente ao second
                    if '"' in coordinate:
                        self.coordinate[coord_name]["second"] = coordinate.replace('"', "").replace(",", ".")
                        self.coordinate[coord_name]["second"] = float(self.coordinate[coord_name]["second"])
                    elif split_value.index(coordinate) == 2:
                        self.coordinate[coord_name]["second"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["second"] = float(self.coordinate[coord_name]["second"])

                # Caso a coordinate esteja em formato degree por minute.
                if spaces == 1:

                    # Referente ao degree.
                    if ("°" in coordinate) or ("º" in coordinate):
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                    elif split_value.index(coordinate) == 0:
                        self.coordinate[coord_name]["degree"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])

                    # Referente ao minute.
                    if "'" in coordinate:
                        self.coordinate[coord_name]["minute"] = coordinate.replace("'", "").replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])
                    elif split_value.index(coordinate) == 1:
                        self.coordinate[coord_name]["minute"] = coordinate.replace(",", ".")
                        self.coordinate[coord_name]["minute"] = float(self.coordinate[coord_name]["minute"])

                # Caso a coordinate esteja em formato de degree/Decimal
                if spaces == 0:

                    # Referente ao degree/decimal
                    if ("°" in coordinate) or ("º" in coordinate):
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]
                    else:
                        self.coordinate[coord_name]["degree"] = coordinate.replace("°", "").replace(",", ".")
                        self.coordinate[coord_name]["degree"] = float(self.coordinate[coord_name]["degree"])
                        self.coordinate[coord_name]["decimal"] = self.coordinate[coord_name]["degree"]

    def get_Latitude (self):
        return self.coordinate["latitude"]

    def get_Longitude (self):
        return self.coordinate["longitude"]

    def Reset_Values (self):
        self.coordinate = {
            "latitude":
                {
                    "degree": None,
                    "minute": None,
                    "second": None,
                    "hemisphere": None,
                    "decimal": None
                },
            "longitude":
                {
                    "degree": None,
                    "minute": None,
                    "second": None,
                    "hemisphere": None,
                    "decimal": None
                }
        }

    def get_Coordinate_List (self):
        return self.coordinate_list

    def Convert_Lat_Decimal (self, lat):
        convert_lat = "Nada"
        convert_lat_list = []
        if type(lat) == str:
            self.Reset_Values()
            self.Format_Lat_Lng(lat, "latitude")

            if self.get_Latitude()["decimal"] == None:

                if self.get_Latitude()["second"] == None:

                    convert_lat = self.get_Latitude()["degree"]
                    helper_value_sec = self.get_Latitude()["minute"] / 60

                    if "-" in str(self.get_Latitude()["degree"]):

                        convert_lat *= -1
                        convert_lat = convert_lat + helper_value_sec
                        convert_lat *= -1

                    else:

                        convert_lat += helper_value_sec

                else:

                    convert_lat = self.get_Latitude()["degree"]
                    helper_value_sec = self.get_Latitude()["second"] / 60
                    helper_value_min = self.get_Latitude()["minute"] + helper_value_sec
                    helper_value_min /= 60

                    if "-" in str(convert_lat):
                        convert_lat *= -1
                        convert_lat = convert_lat + helper_value_min
                        convert_lat *= -1
                    else:
                        convert_lat += helper_value_min
            else:

                convert_lat = self.get_Latitude()["decimal"]

            return convert_lat
        elif type(lat) == list:

            for l in lat:
                if l=="":
                    convert_lat_list.append("")
                    continue
                self.Reset_Values()
                self.Format_Lat_Lng(l, "latitude")
                if self.get_Latitude()["decimal"] == None:

                    if self.get_Latitude()["second"] == None:

                        convert_lat = self.get_Latitude()["degree"]
                        helper_value_sec = self.get_Latitude()["minute"] / 60

                        if "-" in str(self.get_Latitude()["degree"]):

                            convert_lat *= -1
                            convert_lat = convert_lat + helper_value_sec
                            convert_lat *= -1

                        else:

                            convert_lat += helper_value_sec
                    else:

                        convert_lat = self.get_Latitude()["degree"]
                        helper_value_sec = self.get_Latitude()["second"] / 60
                        helper_value_min = self.get_Latitude()["minute"] + helper_value_sec
                        helper_value_min /= 60

                        if "-" in str(convert_lat):

                            convert_lat *= -1
                            convert_lat = convert_lat + helper_value_min
                            convert_lat *= -1

                        else:

                            convert_lat += helper_value_min
                else:

                    convert_lat = self.get_Latitude()["decimal"]
                convert_lat_list.append(convert_lat)
                if (convert_lat == -72.95):
                    print(self.get_Latitude())
            return convert_lat_list

    def Convert_Lng_Decimal(self, lng):

        convert_lng = "Nada"
        convert_lng_list = []

        if type(lng) == str:

            self.Reset_Values()
            self.Format_Lat_Lng(lng, "longitude")

            if self.get_Longitude()["decimal"] == None:

                if self.get_Longitude()["second"] == None:

                    convert_lng = self.get_Longitude()["degree"]
                    helper_value_sec = self.get_Longitude()["minute"] / 60

                    if "-" in str(self.get_Longitude()["degree"]):

                        convert_lng *= -1
                        convert_lng = convert_lng + helper_value_sec
                        convert_lng *= -1

                    else:

                        convert_lng += helper_value_sec

                else:

                    convert_lng = self.get_Longitude()["degree"]
                    helper_value_sec = self.get_Longitude()["second"] / 60
                    helper_value_min = self.get_Longitude()["minute"] + helper_value_sec
                    helper_value_min /= 60

                    if "-" in str(convert_lng):

                        convert_lng *= -1
                        convert_lng = convert_lng + helper_value_min
                        convert_lng *= -1

                    else:

                        convert_lng += helper_value_min
            else:

                convert_lng = self.get_Longitude()["decimal"]

            return convert_lng
        elif type(lng) == list:

            for l in lng:
                if l=="":
                    convert_lng_list.append("")
                    continue
                self.Reset_Values()
                self.Format_Lat_Lng(l, "longitude")

                if self.get_Longitude()["decimal"] == None:

                    if self.get_Longitude()["second"] == None:

                        convert_lng = self.get_Longitude()["degree"]
                        helper_value_sec = self.get_Longitude()["minute"] / 60

                        if "-" in str(self.get_Longitude()["degree"]):

                            convert_lng *= -1
                            convert_lng = convert_lng + helper_value_sec
                            convert_lng *= -1

                        else:

                            convert_lng += helper_value_sec

                    else:

                        convert_lng = self.get_Longitude()["degree"]
                        helper_value_sec = self.get_Longitude()["second"] / 60
                        helper_value_min = self.get_Longitude()["minute"] + helper_value_sec
                        helper_value_min /= 60

                        if "-" in str(convert_lng):

                            convert_lng *= -1
                            convert_lng = convert_lng + helper_value_min
                            convert_lng *= -1

                        else:

                            convert_lng += helper_value_min
                else:

                    convert_lng = self.get_Longitude()["decimal"]

                convert_lng_list.append(convert_lng)

            return convert_lng_list
