from muslimDeen.model_surah import ModelSurah
from muslimDeen.model_name import ModelName


class Model:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.__model_name = None
        self.__model_surah = None

    @property
    def model_name(self) -> ModelName:
        if self.__model_name is None:
            self.__model_name = ModelName(self.path_database)
        return self.__model_name

    @property
    def model_surah(self) -> ModelSurah:
        if self.__model_surah is None:
            self.__model_surah = ModelSurah(self.path_database)
        return self.__model_surah
