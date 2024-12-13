import muslimDeen.meta_quran_reader as metaquranreader
from typing import Tuple, Callable
from concurrent.futures import ThreadPoolExecutor


class DatasetModel:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.meta_quran = metaquranreader.MetaQuranReader(self.path_database)

    def dataset_name_fr(self, func: Callable) -> Tuple[list, dict]:
        dataset = []
        mapping_original = {}
        for _, v in self.meta_quran.lower_name_fr.items():
            original = v["nom_sourate"]
            cleaned = func(original)
            dataset.append(cleaned)
            mapping_original[cleaned] = original
        return dataset, mapping_original

    def process_sourate(self, item, func):
        _, v = item
        original = v["nom_sourate"]
        versets = self.meta_quran.get_versets(v, 'fr', return_types="list")
        dataset = []
        for i, verset in enumerate(versets, start=1):
            cleaned = func(verset)
            dataset.append({"sourate": original, "verset_position": i, "verset_text": cleaned})
        return dataset


    def dataset_text_quran_fr(self, func: Callable):
        dataset = []
        sourates = list(self.meta_quran.lower_name_fr.items())

        with ThreadPoolExecutor() as executor:
            results = executor.map(
                lambda item: self.process_sourate(item, func), sourates)
            for result in results:
                dataset.extend(result)
        return dataset

