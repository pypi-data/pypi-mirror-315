from datetime import datetime
from pathlib import Path
import torch as tr
from torch import nn

import typer
from loguru import logger

from srcmlmal.config import MODELS_DIR, PROCESSED_DATA_DIR
from srcmlmal.dataset import CaesarDataset, DataLoader
from srcmlmal.modeling.trainer import Trainer
from models.caesar_models.LSTM import LSTMClassifier

app = typer.Typer()


@app.command()
def train_model(old: bool = False):
    data_file = "caesar_data.csv"
    caesar_dataset = CaesarDataset(
        step=2,
        path_to_file=f"{
            PROCESSED_DATA_DIR}/{data_file}",
    )

    train_amount = 0.7
    val_amount = 0.5

    trainn = int(len(caesar_dataset) * train_amount)
    valn = int((len(caesar_dataset) - trainn) * val_amount)
    testn = len(caesar_dataset) - trainn - valn
    train_data, val_data, test_data = tr.utils.data.random_split(
        caesar_dataset, [trainn, valn, testn]
    )

    train: DataLoader = DataLoader(train_data, batch_size=16, shuffle=True)
    val: DataLoader = DataLoader(val_data, batch_size=16, shuffle=True)
    test: DataLoader = DataLoader(test_data, batch_size=16, shuffle=False)

    classn = len(caesar_dataset.caesar_dict)
    emb_size = 1
    fan_in, fan_out = emb_size, classn
    LSTM = LSTMClassifier(
        classn=classn,
        embsize=1,
    )

    curr_exp_models_dir = "caesar_models"
    model_name = "caesar_classifier.pth"
    if old:
        model = tr.load(
            f"{MODELS_DIR}/{curr_exp_models_dir}/{model_name}", weights_only=False)
    else:
        model = LSTM

    epochn = 1
    lr = 1e-4

    lossf = nn.CrossEntropyLoss()
    opt = tr.optim.RMSprop(model.parameters(), lr=lr)
    sch = tr.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer=opt, T_0=10)

    device = tr.device("cuda") if tr.cuda.is_available() else tr.device("cpu")

    train_dataloader = train
    val_dataloader = val
    test_dataloader = test

    config = {
        "model": model,
        "lossf": lossf,
        "opt": opt,
        "sch": sch,
        "epochn": epochn,
        "device": device,
        "train_dataloader": train_dataloader,
        "val_dataloader": val_dataloader,
        "test_dataloader": test_dataloader,
    }

    trainer = Trainer(**config)
    trainer.train()
    tr.save(model, f"{MODELS_DIR}/{curr_exp_models_dir}/{model_name}")


if __name__ == "__main__":
    app()
