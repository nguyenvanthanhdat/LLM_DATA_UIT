from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from sentence_transformers.losses import TripletLoss, ContrastiveLoss, CosineSimilarityLoss
from torch.nn import CrossEntropyLoss 
import torch

class CrossEntropyLossTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop("labels")
        # forward pass
        # outputs = model(**inputs)
        outputs = model({'input_ids': inputs['input_ids'], 'attention_mask': inputs['attention_mask']})
        logits = outputs.get("logits")
        loss_fct = CrossEntropyLoss()
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss
