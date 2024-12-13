from muslimDeen.meta_quran_reader import MetaQuranReader
from muslimDeen.model import Model
from muslimDeen.interface import QuranSourateData, QuranVersetData
from muslimDeen.handle_exception import SurahNotFound
from typing import Union, Tuple, Literal, Optional, List
import pathlib as plib


class MetaQuranReaderModel(MetaQuranReader):
    def __init__(self, path_database: str):
        super().__init__(path_database)
        self.model = Model(self.path_database)

    def search_fr(self, predicate_user: str, get_score=False) -> Union[Tuple[Optional[QuranSourateData], str | None], QuranSourateData, None]:
        predicate, score = self.model.model_name.predicate(predicate_user)
        if get_score:
            return predicate, score
        return predicate

    def get_surah(
        self,
        predicate: Optional[str] = None,
        name: Optional[str] = None,
        write_in_file: bool = False,
        output_file: Optional[Union[str, plib.Path]] = None,
        language: Optional[Literal["fr", "arabic"]] = None
    ):
        surah: QuranSourateData = None
        if predicate and name is None:
            surah = self.search_fr(predicate)
        elif predicate is None and name:
            surah_name = self.search_by_name_fr(name)
            if surah_name is None:
                raise SurahNotFound("Surah not found")
            surah = surah_name[0]
        else:
            surah = self.search_fr(predicate)

        if surah is None:
            raise SurahNotFound("Surah not found")

        if language not in ("fr", "arabic"):
            language = "fr"

        versets = self.get_versets(surah, language, "str")

        if write_in_file:
            if output_file is None:
                current_word_directory = plib.Path().cwd()
                output_file = current_word_directory / \
                    f"{surah['nom_sourate']}-{language}.txt"
            else:
                output_file = plib.Path(output_file)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file = output_file / \
                    f"{surah['nom_sourate']}-{language}.txt"
            self.write_file_surah(output_file, versets)
        return surah, versets

    def write_file_surah(self, output_file: str, versets: str, encoding: str = "utf-8-sig") -> None:
        try:
            with open(output_file, "w", encoding=encoding) as file:
                file.write(versets)
        except KeyError:
            raise KeyError("Key not found in dict 'versets'")
        except IOError:
            raise IOError("Error writting file")

    def search(self, input_text: str) -> List[Tuple[Optional[QuranSourateData], int, Optional[QuranVersetData]]]:
        predicate_surah = self.model.model_surah.predicate(input_text)
        return predicate_surah
