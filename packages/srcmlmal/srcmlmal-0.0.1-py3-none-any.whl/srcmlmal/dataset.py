import string
import torch as tr
import pandas as pd
import numpy as np
from torch.utils.data import Dataset


class CaesarDataset(Dataset):
    def __init__(self, step, path_to_file):
        self.caesar_dict = self.generate_caesar_dictionary(step=step)
        self.stoi = self.generate_stoi()
        self.itos = self.generate_itos()
        self.dataset = self.generate_dataset(path_to_file=path_to_file)

    def __len__(self):
        return len(self.dataset["X"])

    def __getitem__(self, ix):
        return self.dataset["X"][ix], self.dataset["Y"][ix]

    def generate_caesar_dictionary(self, step: int) -> dict[str:str]:
        alph_lower = list(string.ascii_lowercase)
        caesar_dict_lower = {
            ch: alph_lower[(ix + step) % len(alph_lower)] for ix, ch in enumerate(alph_lower)
        }

        alph_upper = list(string.ascii_uppercase)
        caesar_dict_upper = {
            ch: alph_upper[(ix + step) % len(alph_upper)] for ix, ch in enumerate(alph_upper)
        }

        caesar_dict = {}
        for k, v in caesar_dict_lower.items():
            caesar_dict[k] = v
        for k, v in caesar_dict_upper.items():
            caesar_dict[k] = v

        return caesar_dict

    def word_to_caesar(self, word: str) -> str:
        encoded = [self.caesar_dict[ch] for ch in word]
        encoded = "".join(encoded)
        return encoded

    def generate_stoi(self):
        alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        stoi = {ch: ix for ix, ch in enumerate(alphabet)}

        return stoi

    def generate_itos(self):
        alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        itos = {ix: ch for ix, ch in enumerate(alphabet)}
        return itos

    def generate_dataset(self, path_to_file: str):
        dt = pd.read_csv(path_to_file)
        words_raw = dt["word"].to_numpy()
        words = list(words_raw[type(words_raw) != float].squeeze(0))[:]
        dataset = {"X": [], "Y": []}

        for ix, word in enumerate(words):
            if word is not np.nan:
                x, y = self.word_to_caesar(word), word
                for ch in x:
                    dataset["X"].append(self.stoi[ch])
                for ch in y:
                    dataset["Y"].append(self.stoi[ch])

        dataset["X"] = tr.tensor(dataset["X"]).type(tr.float32).view(-1, 1)
        dataset["Y"] = tr.tensor(dataset["Y"]).type(tr.long)
        return dataset
