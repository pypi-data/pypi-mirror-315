from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import torch as tr
import pandas as pd

from srcmlmal.config import MODELS_DIR, PROCESSED_DATA_DIR
from srcmlmal.dataset import CaesarDataset
from torch.utils.data import DataLoader

app = typer.Typer()


@app.command()
def main(
    features_path: Path = PROCESSED_DATA_DIR / "test_features.csv",
    model_path: Path = MODELS_DIR / "caesar_models" / "caesar_classifier.pth",
    predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv",
):
    """
    Load a trained model and run inference on test data.
    The test_features.csv is expected to have a 'word' column with words.
    For each character in these words, we run the model and predict the output character.
    Predictions are saved as a single column 'prediction' in test_predictions.csv.
    """

    logger.info(f"Loading model from: {model_path}")
    device = tr.device("cuda") if tr.cuda.is_available() else tr.device("cpu")

    # Load the trained model
    model = tr.load(model_path, map_location=device)
    model.eval()

    # Load dataset
    logger.info(f"Loading test data from: {features_path}")
    # Assume step=2 as in train.py. Adjust if necessary.
    caesar_dataset = CaesarDataset(step=2, path_to_file=str(features_path))

    test_loader = DataLoader(caesar_dataset, batch_size=16, shuffle=False)

    predictions = []

    logger.info("Starting inference...")
    with tr.no_grad():
        for features, _ in tqdm(test_loader):
            features = features.to(device)
            pred = model(features)  # pred shape: [batch_size, classn]

            # Get predicted class (argmax)
            pred_class = pred.argmax(dim=1).cpu().numpy()

            # Convert class indices back to chars using dataset.itos
            for pc in pred_class:
                predictions.append(caesar_dataset.itos[pc])

    # Save predictions to CSV
    # Since the dataset is a sequence of characters, predictions is just a list of chars.
    # If you want to reconstruct words, you'd have to know how to chunk them.
    # For now, we will just output one predicted character per line.
    df = pd.DataFrame({"prediction": predictions})
    df.to_csv(predictions_path, index=False)
    logger.info(f"Predictions saved to: {predictions_path}")


if __name__ == "__main__":
    app()
