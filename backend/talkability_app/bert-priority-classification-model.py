from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import DataCollatorWithPadding
from sklearn.model_selection import train_test_split
import pandas as pd

# Load the data
df = pd.read_csv('../training/datasets-priority/requests.csv')

# Split the data into train and test sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert to Hugging Face datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Create the DatasetDict
dataset_dict = DatasetDict({
    "train": train_dataset,
    "test": test_dataset
})

# Load pre-trained model and tokenizer (BERT)
model_path = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.save_pretrained("./training/bert-urgency-classification")

id2label = {
    0: "Urgent", 1: "Normal", 2: "Light"
}
label2id = {v: k for k, v in id2label.items()}  # Reversing id2label for label2id

model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=3, id2label=id2label, label2id=label2id)

# Freeze all base model parameters
for name, param in model.base_model.named_parameters():
    param.requires_grad = False

# Unfreeze base model pooling layers
for name, param in model.base_model.named_parameters():
    if "pooler" in name:
        param.requires_grad = True

# Tokenization function with label conversion
def preprocess_function(examples):
    # Clean the labels by stripping extra spaces and removing any unwanted quotation marks
    examples['label'] = [label.strip().replace('"', '') for label in examples['label']]
    examples['label'] = [label2id[label] for label in examples['label']]
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# Tokenize the dataset
tokenized_data = dataset_dict.map(preprocess_function, batched=True)

# Data collator for padding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir="../talkability_app/bert-urgency-classification",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    logging_strategy="epoch",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Fine-tune the model
trainer.train()