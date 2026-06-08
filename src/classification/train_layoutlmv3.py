import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import json
from pathlib import Path

import pandas as pd
import torch
from PIL import Image
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

from transformers import (
    LayoutLMv3ForSequenceClassification,
    LayoutLMv3Processor,
    Trainer,
    TrainingArguments,
)


LABELS = [
    "bill_of_lading",
    "commercial_invoice",
    "letter_of_credit",
    "packing_list",
]

label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for label, i in label2id.items()}


class TradeFinanceLayoutDataset(Dataset):
    def __init__(self, dataframe, processor):
        self.df = dataframe.reset_index(drop=True)
        self.processor = processor

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        image = Image.open(row["image_path"]).convert("RGB")

        with open(row["layout_path"], "r") as f:
            layout = json.load(f)

        words = [w["word"] for w in layout["words"]]
        boxes = [w["bbox"] for w in layout["words"]]

        if len(words) == 0:
            words = ["empty"]
            boxes = [[0, 0, 0, 0]]

        encoding = self.processor(
            image,
            words,
            boxes=boxes,
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt",
        )

        item = {k: v.squeeze(0) for k, v in encoding.items()}
        item["labels"] = torch.tensor(label2id[row["doc_type"]], dtype=torch.long)

        return item


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    return {"accuracy": accuracy_score(labels, preds)}


def main():
    manifest = pd.read_csv("data/processed/manifest.csv")

    manifest = manifest[manifest["doc_type"].isin(LABELS)].copy()

    train_df, test_df = train_test_split(
        manifest,
        test_size=0.2,
        random_state=42,
        stratify=manifest["doc_type"],
    )

    processor = LayoutLMv3Processor.from_pretrained(
        "microsoft/layoutlmv3-base",
        apply_ocr=False,
    )

    train_dataset = TradeFinanceLayoutDataset(train_df, processor)
    test_dataset = TradeFinanceLayoutDataset(test_df, processor)

    model = LayoutLMv3ForSequenceClassification.from_pretrained(
        "microsoft/layoutlmv3-base",
        num_labels=len(LABELS),
        label2id=label2id,
        id2label=id2label,
    )

    training_args = TrainingArguments(
        output_dir="models/layoutlmv3-trade-doc-classifier",
        eval_strategy="epoch", 
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_steps=10,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    predictions = trainer.predict(test_dataset)
    preds = predictions.predictions.argmax(axis=-1)

    print(classification_report(
        predictions.label_ids,
        preds,
        target_names=LABELS,
    ))

    trainer.save_model("models/layoutlmv3-trade-doc-classifier/final")
    processor.save_pretrained("models/layoutlmv3-trade-doc-classifier/final")

    print("Saved model to models/layoutlmv3-trade-doc-classifier/final")


if __name__ == "__main__":
    main()