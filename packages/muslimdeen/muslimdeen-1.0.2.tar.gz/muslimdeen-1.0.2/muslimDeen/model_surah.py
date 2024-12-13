from sentence_transformers import SentenceTransformer
import faiss
from rapidfuzz import fuzz
from symspellpy import SymSpell, Verbosity
import pathlib as plib
import numpy as np
from muslimDeen.datasetmodel import DatasetModel
from muslimDeen.utils_model import download_hunspell, convert_hunspell_to_symspell, output_file_hunspell, hunspell_file, clear_text, weighted_similarity_score
from muslimDeen.interface import QuranSourateData, QuranVersetData
from typing import List, Tuple, Optional


class ModelSurah:
    def __init__(self, path_database: str):
        self.path_database = path_database
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self._setup_symspell()

        self.dataset_model = DatasetModel(self.path_database)
        dataset, mapping_original = self._load_dataset()
        self.__dataset_text_fr = dataset
        self.__mapping_original_fr = mapping_original

        self.__embeddings_base = self._encode_dataset(dataset)
        self.__index = self._configure_faiss(self.__embeddings_base)

    def _setup_symspell(self):
        download_hunspell(self.path_database)
        convert_hunspell_to_symspell(
            self.path_database, hunspell_file, output_file_hunspell)
        self.sym_spell = SymSpell(
            max_dictionary_edit_distance=2, prefix_length=7)
        self.sym_spell.load_dictionary(plib.Path(self.path_database).joinpath(
            output_file_hunspell), term_index=0, count_index=1)

    def _load_dataset(self):
        dataset = self.dataset_model.dataset_text_quran_fr(clear_text)
        texts = [item["verset_text"] for item in dataset]
        mapping = {
            item["verset_text"]: {
                "sourate": item["sourate"],
                "position": item["verset_position"]
            } for item in dataset
        }
        return texts, mapping

    def _encode_dataset(self, dataset):
        embeddings = self.model.encode(dataset)
        embeddings = embeddings / \
            np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings

    def _configure_faiss(self, embeddings):
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        return index

    @property
    def dataset_text_fr(self):
        return self.__dataset_text_fr

    @property
    def mapping_original_fr(self):
        return self.__mapping_original_fr

    def correct_spelling(self, input_text: str) -> str:
        suggestions = self.sym_spell.lookup(
            input_text, Verbosity.CLOSEST, max_edit_distance=2)
        return suggestions[0].term if suggestions else input_text

    def find_similar_versets(self, input_text: str, top_k: int = 5, threshold: float = 0.15):
        corrected_text = self.correct_spelling(input_text)
        cleaned_text = clear_text(corrected_text)
        embedding_user = self.model.encode([cleaned_text])
        embedding_user = embedding_user / \
            np.linalg.norm(embedding_user, axis=1, keepdims=True)

        distances, indices = self.__index.search(embedding_user, k=top_k)
        candidates = [(self.dataset_text_fr[i], distances[0][j])
                      for j, i in enumerate(indices[0]) if distances[0][j] > threshold]

        if not candidates:
            return [{"sourate": "Aucune correspondance trouvée", "position": None, "verset": None, "score": 0.0}]
        results = []
        for candidate, faiss_distance in candidates:
            fuzzy_score = fuzz.ratio(cleaned_text, candidate)
            combined_score = weighted_similarity_score(
                faiss_distance, fuzzy_score)
            sourate_info = self.mapping_original_fr[candidate]
            results.append({
                "sourate": sourate_info["sourate"],
                "position": sourate_info["position"],
                "verset": candidate,
                "score": combined_score
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def predicate(self, input_user: str) -> List[Tuple[Optional[QuranSourateData], int, Optional[QuranVersetData]]]:
        versets_predicate = self.find_similar_versets(input_user)
        results = []
        for verset_predicate in versets_predicate:
            surah = verset_predicate['sourate']
            position: int = verset_predicate['position']
            s_target = self.dataset_model.meta_quran.get_name_fr(surah)[0]
            s, v = self.dataset_model.meta_quran.get(
                f"{s_target['position']}:{position}")
            results.append((s, position, v))
        return results
