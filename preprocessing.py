import os
import re

import PyPDF2
from sklearn.model_selection import train_test_split

# pdf_file_paths = list(os.listdir("LLM Project"))

# # Step 2: Text Extraction

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(f'LLM Project/{pdf_path}', 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()
#     return text

# property_texts = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_file_paths]

# print("property_texts----------->",property_texts)

# # Step 3: Text Preprocessing

# def preprocess_text(text):
#     # Remove special characters and extra whitespace
#     text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# # property_texts = [preprocess_text(text) for text in property_texts]
# # with open("preprocessed_data.txt", 'w') as f:
# #     f.write(str(property_texts))
# #     f.close()

# # print(property_texts)
# # Step 4: Data Splitting

# # Split the data into training, validation, and test sets
# train_texts, test_texts = train_test_split(property_texts, test_size=0.15, random_state=42)
# train_texts, val_texts = train_test_split(train_texts, test_size=0.15, random_state=42)

# # with open("training_data.txt", 'w') as f:
# #     f.write(str(train_texts))
# #     f.close()

# # with open("val_data.txt", 'w') as f:
# #     f.write(str(val_texts))
# #     f.close()

# # # Step 5: Model Selection
from transformers import GPT2Tokenizer, GPT2LMHeadModel

model_name = "gpt2" 
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

from transformers import TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# # # Create a TextDataset
# # train_dataset = TextDataset(
# #     tokenizer=tokenizer,
# #     file_path="E:/LLM Project-20230923T054733Z-001/training_data.txt", 
# #     block_size=128, 
# # )

# Create a DataCollator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,
)

# # # Define training arguments
# # training_args = TrainingArguments(
# #     per_device_train_batch_size=4,
# #     num_train_epochs=3,
# #     evaluation_strategy="steps",
# #     eval_steps=100,
# #     save_steps=1000,
# #     output_dir="E:/LLM Project-20230923T054733Z-001/property_model",
# # )

# # val_dataset = TextDataset(
# #     tokenizer=tokenizer,
# #     file_path="E:/LLM Project-20230923T054733Z-001/val_data.txt",  
# #     block_size=128,  
# # )

# # eval_data_collator = DataCollatorForLanguageModeling(
# #     tokenizer=tokenizer,
# #     mlm=False,  
# # )

# # evaluation_args = TrainingArguments(
# #     per_device_eval_batch_size=4,
# #     output_dir="E:/LLM Project-20230923T054733Z-001/property_model",
# # )
# # # Create a Trainer
# # trainer = Trainer(
# #     model=model,
# #     args=evaluation_args,
# #     data_collator=eval_data_collator, 
# #     train_dataset=train_dataset,
# #     eval_dataset=val_dataset,  
# # )

# # Fine-tune the model
# # trainer.train()

# # Step 7: Evaluation (Optional)
# # Load the validation dataset
# # val_dataset = TextDataset(
# #     tokenizer=tokenizer,
# #     file_path=None,  # Provide the path to a text file with your validation data
# #     block_size=128,  # Adjust the block size as needed
# # )

# # Create a Trainer for evaluation
# # evaluation_args = TrainingArguments(
# #     per_device_eval_batch_size=4,
# #     output_dir="./property_model",
# # )

# # trainer = Trainer(
# #     model=model,
# #     args=evaluation_args,
# #     data_collator=data_collator,
# #     eval_dataset=val_dataset,  # Use the validation dataset
# # )

# # Evaluate the model
# # eval_results = trainer.evaluate()

# # print(eval_results)
# # You can evaluate the model on a validation dataset to monitor its performance.

# # Step 8: Hyperparameter Tuning (Optional)
import optuna

# Define a function to optimize hyperparameters
# def objective(trial):
#     # Define hyperparameters to search over
#     learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-3)
#     batch_size = trial.suggest_int("batch_size", 2, 32)
    
#     # Define TrainingArguments with suggested hyperparameters
#     training_args = TrainingArguments(
#         per_device_train_batch_size=batch_size,
#         learning_rate=learning_rate,
#         num_train_epochs=3,
#         evaluation_strategy="steps",
#         eval_steps=100,
#         save_steps=1000,
#         output_dir="E:/LLM Project-20230923T054733Z-001/property_model",
#     )

#     eval_dataset = TextDataset(
#         tokenizer=tokenizer,
#         file_path="E:/LLM Project-20230923T054733Z-001/val_data.txt", 
#         block_size=128,
#     )

#     train_dataset = TextDataset(
#         tokenizer=tokenizer,
#         file_path="E:/LLM Project-20230923T054733Z-001/training_data.txt", 
#         block_size=128,
#     )

#     # Create and train the model
#     trainer = Trainer(
#         model=model,
#         args=training_args,
#         data_collator=data_collator,
#         train_dataset=train_dataset,
#         eval_dataset=eval_dataset, 
#     )
#     trainer.train()


#     # Evaluate the model
#     eval_results = trainer.evaluate()

#     # Evaluate the model on the validation dataset
#     # eval_results = trainer.evaluate()
#     return eval_results["eval_loss"]

# # Optimize hyperparameters
# study = optuna.create_study(direction="minimize")
# study.optimize(objective, n_trials=10)  # Adjust the number of trials as needed

# # Get the best hyperparameters
# best_params = study.best_params
# print("Best Hyperparameters:", best_params)

# Fine-tune hyperparameters as needed, e.g., learning rate, batch size.

# Step 9: Content Generation
from transformers import GPT2Tokenizer, pipeline

# Load the fine-tuned model for content generation
model_directory = "E:/LLM Project-20230923T054733Z-001/property_model/checkpoint-1000"
tokenizer = GPT2Tokenizer.from_pretrained(model_directory)
generator = pipeline("text-generation", model=model_directory)

# Example property detail
property_detail = "This is a beautiful 3-bedroom house with a spacious backyard."

# Generate content based on the property detail
generated_text = generator(property_detail, max_length=100, num_return_sequences=1, temperature=0.7)

# Print the generated text
print(generated_text[0]['generated_text'])



