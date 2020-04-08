import os
import xlrd
from xlutils.copy import copy
from model.coordinate import Coordinate
from model.data_treatment import Data_Treatment
from model.locality import Locality
import xlwt


class Sheet:

    def __init__(self):
        # Essas variáveis irão ser atribuídas assim que o objeto for criado, pois dizem respeito somente ao arquivo, então já configuro eles automaticamente.
        self.path = None
        self.file = None
        self.write_file = None
        self.sheet_list = None
        self.sheet = None
        self.formated_sheet = None
        self.coordinate = None
        self.locality = None
        self.data_treatment = None
        self.columns_total = int
        self.row_total = int
        self.cell_value = str
        self.values_column = []
        self.values_row = []
        self.index_sheet = 0

    def set_Path_configure_all(self, path):
        self.path = str(
            os.getcwd()) + "/files/" + path if path != None else None  # O comando os.getcwd pega o diretório atual de onde o arquivo python está.

        try:
            self.file = xlrd.open_workbook(self.path,
                                           formatting_info=True)  # Abre o arquivo com o nome enviado no parâmetro diretorio
        except:
            self.file = xlrd.open_workbook(self.path)  # Abre o arquivo com o nome enviado no parâmetro diretorio
        self.write_file = copy(self.file)
        xlwt.add_palette_colour("custom_colour", 0x21)
        self.sheet_list = self.file.sheet_names()  # Pega o nome das páginas do arquivo
        self.sheet = self.file.sheet_by_index(0)  # Pega a página inicial (começa por 0)
        self.formated_sheet = self.write_file.get_sheet(0)
        # Aqui já vão ser atribuídas no decorrer do processamento.
        self.columns_total = self.sheet.ncols
        self.row_total = self.sheet.nrows
        self.coordinate = Coordinate(self.sheet)
        self.data_treatment = Data_Treatment(self.sheet)
        self.locality = Locality(self.sheet)

    def set_Path(self, path):
        self.path = str(os.getcwd()) + "/files/" + path if path != None else None

    def get_Path(self):
        return self.path

    def set_File(self, file):
        self.file = file

    def get_Sheet(self):
        return self.sheet_list[self.index_sheet]

    def get_Sheet_List(self):
        self.sheet_list = self.file.sheet_names()
        return self.sheet_list

    def get_Sheet_Header(self):
        return self.sheet.row_values(0)

    def get_Columns_Total(self):
        return self.columns_total

    def get_Row_Total(self):
        return self.row_total

    def Value_in_Cell(self, row, columns):
        if (row > self.get_Row_Total()):
            return "Linha excede valor total de linhas do arquivo."
        if (columns > self.get_Columns_Total()):
            return "Coluna excede valor total de colunas do arquivo."
        if (row <= self.get_Row_Total() and columns <= self.get_Columns_Total()):
            self.cell_value = self.sheet.cell(row, columns).value
            return self.cell_value

    def Value_in_Column(self, column):
        self.Reset_Values()
        try:
            if (type(column) == str):
                index_column = self.sheet.row_values(0).index(column)
                self.values_column = self.sheet.col_values(index_column, 1)
                if (self.values_column == []):
                    return "Not found."
                else:
                    return self.values_column
            elif (type(column) == int):
                self.values_column = self.sheet.col_values(column, 1)
                return self.values_column
        except:
            return "Not found."

    def Value_in_Row(self, row):
        if (row <= self.get_Row_Total() and row > 0):
            self.Resetar_Values()
            self.values_row = self.sheet.row_values((row - 1))
            return self.values_row
        else:
            return "Linha excede limite de linhas do documento."

    def Reset_Values(self):
        self.cell_value = str
        self.values_column = []
        self.values_row = []

    def set_Check_Columns(self, titles):
        self.data_treatment.Reset_Values()
        for column in titles:
            if titles[column] != None:
                values_column = self.Value_in_Column(titles[column])
                self.data_treatment.set_Original_Titles(titles[column])
                self.data_treatment.set_Check_Columns(column, values_column)

    def get_Columns_Checked(self):
        return self.data_treatment.get_Validate_Columns()

    def Change_Data_Spreadsheet(self, data_to_change):
        for values in data_to_change:
            key1 = values
            for data in data_to_change[values]:
                level = data_to_change[values][data]["level"][0]
                column_index = self.sheet.row_values(0).index(
                    self.data_treatment.get_Verified_Hierarchy()[key1][data]["title"])
                column_index_level = self.sheet.row_values(0).index(
                    self.data_treatment.get_Verified_Hierarchy()[key1][level]["title"])
                for row in range(0, self.get_Row_Total()):
                    value1 = self.data_treatment.get_Verified_Hierarchy()[key1][data]["type"]
                    value2 = self.Value_in_Cell(row, column_index)
                    value1_level = data_to_change[values][data]["level"][1]
                    value2_level = self.Value_in_Cell(row, column_index_level)
                    if ((value1 == value2) and (value1_level == value2_level)):
                        style = xlwt.easyxf(
                            'pattern: pattern solid, fore_colour green; font: colour white; borders: left 1, right 1, top 1, bottom 1; font: bold 1;')
                        self.formated_sheet.write(row, column_index, data_to_change[key1][data]["suggestion"], style)

    def Change_Data_Spreadsheet2(self, data_to_change):
        for row in data_to_change:
            for column in data_to_change[row]:
                column_index = self.sheet.row_values(0).index(column)
                change_row = int(row) - 1
                style = xlwt.easyxf(
                    'pattern: pattern solid, fore_colour green; font: colour white; borders: left 1, right 1, top 1, bottom 1; font: bold 1;')
                self.formated_sheet.write(change_row, column_index, data_to_change[row][column], style)

    def Save_Formatted_Spreadsheet(self):
        return self.write_file.save("files/Planilha_Formatada.xls")
