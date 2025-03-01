from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import DataCollatorWithPadding
from sklearn.model_selection import train_test_split
import pandas as pd

# ✅ Load the data correctly
df = pd.read_csv('../training/datasets/requests.csv', quotechar='"', skipinitialspace=True)

# ✅ Check if 'label' exists and is mapped correctly
print(df.head())
print(df.dtypes)

# ✅ Define label mapping
id2label = {
    0: "Technical Support", 1: "Billing", 2: "Sales",
    3: "Appointments", 4: "Medical Records", 5: "Pharmacy",
}
label2id = {v: k for k, v in id2label.items()}  # Reverse mapping

# ✅ Convert text labels to numeric IDs
df['label'] = df['label'].str.strip().map(label2id)

# ✅ Handle any missing or unknown labels
if df['label'].isnull().sum() > 0:
    print("Warning: Some labels were not found in label2id! These will be dropped.")
    df = df.dropna(subset=['label'])  # Remove unknown labels
df['label'] = df['label'].astype(int)  # Ensure labels are integers

print(df['label'].value_counts())  # Check dataset balance

# ✅ Split the data into train and test sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# ✅ Convert to Hugging Face datasets (keep only 'text' and 'label')
train_dataset = Dataset.from_pandas(train_df[['text', 'label']])
test_dataset = Dataset.from_pandas(test_df[['text', 'label']])

# ✅ Create the DatasetDict
dataset_dict = DatasetDict({
    "train": train_dataset,
    "test": test_dataset
})

# ✅ Load pre-trained model and tokenizer (BERT)
model_path = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.save_pretrained("./training/bert-department-classification")

# ✅ Initialize model with correct number of labels
model = AutoModelForSequenceClassification.from_pretrained(
    model_path, num_labels=len(id2label), id2label=id2label, label2id=label2id
)

# ✅ Unfreeze only the classifier head (not the entire model)
for name, param in model.base_model.named_parameters():
    param.requires_grad = False  # Freeze BERT layers
for name, param in model.base_model.named_parameters():
    if "pooler" in name:
        param.requires_grad = True  # Unfreeze pooling layers

# ✅ Tokenization function (now labels are already numbers)
def preprocess_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# ✅ Tokenize the dataset
tokenized_data = dataset_dict.map(preprocess_function, batched=True)

# ✅ Data collator for padding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# ✅ Define Training arguments
training_args = TrainingArguments(
    output_dir="../talkability_app/bert-department-classification",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=8,
    logging_strategy="epoch",
    evaluation_strategy="epoch",
    # save_strategy="epoch",
    # load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    save_total_limit = 2,
    save_strategy = False,
    load_best_model_at_end=False
)

# ✅ Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# ✅ Fine-tune the model
trainer.train()