import json

class DropConfig:
    def __init__(self, month, startdrop, enddrop):
        self.month = month
        self.startdrop = startdrop
        self.enddrop = enddrop

class GenericConfig:
    def __init__(self,mevTypes,mevTypesSelector,outputFile,folderName,outliercsv,customOF,compFile):
        self.mevTypes = mevTypes
        self.mevTypesSelector = mevTypesSelector
        self.outputFiles = outputFile
        self.folderName = folderName
        self.outlierCsv = outliercsv
        self.customOutputFile = customOF
        self.comparisionFile = compFile


class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        with open(self.config_file, 'r') as file:
            self.data = json.load(file)
            self.mev_types = self.data.get('mev_types', [])
            self.mevTypesSelector = self.data.get('mev_types_selector',[])
            self.outputFiles = self.data.get('outputFile')
            self.customOutputFile = self.data.get('customOutputFile')
            self.folderName = self.data.get('folderName')
            self.outlierCsv = self.data.get('outlierFile')
            self.comparisionFile = self.data.get('comparisionFile')

    def getGenericData(self):
        return GenericConfig(self.mev_types,self.mevTypesSelector,self.outputFiles,self.folderName,self.outlierCsv,self.customOutputFile,self.comparisionFile)


    def load_config(self):
        drop_configs = []



        for drop_data in self.data['drops']:
            month = drop_data['month']
            startdrop = drop_data['startdrop']
            enddrop = drop_data['enddrop']
            drop_config = DropConfig(month, startdrop, enddrop)
            drop_configs.append(drop_config)

        return drop_configs
