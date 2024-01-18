from datasets import load_dataset, Dataset, DatasetDict
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, AdamWeightDecay, MarianMTModel, MarianTokenizer,DataCollatorForSeq2Seq
import tensorflow as tf
import warnings

class Translator:
    def __init__(self, source_lang="ja", target_lang="en", model_name="Helsinki-NLP/opus-mt-ja-en"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_input_length = 128
        self.max_target_length = 128
        self.model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)

    def preprocess_function(self, examples):
        inputs = [ex['translation'][self.source_lang] for ex in examples['translation']]
        targets = [ex['translation'][self.target_lang] for ex in examples['translation']]
        model_inputs = self.tokenizer(inputs, max_length=self.max_input_length, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(targets, max_length=self.max_target_length, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def transform_dataset(self, dataset):
        transformed_data = []
        for data_point in dataset:
            transformed_point = {
                "translation": {
                    self.target_lang: data_point[self.target_lang + "_sentence"],
                    self.source_lang: data_point[self.source_lang + "_sentence"]
                }
            }
            transformed_data.append(transformed_point)
        return transformed_data

    def load_and_prepare_datasets(self):
        raw_datasets = load_dataset("bsd_ja_en")

        transformed_train_dataset = self.transform_dataset(raw_datasets["train"])
        transformed_validation_dataset = self.transform_dataset(raw_datasets["validation"])
        transformed_test_dataset = self.transform_dataset(raw_datasets["test"])

        transformed_train = Dataset.from_dict({"translation": transformed_train_dataset})
        transformed_validation = Dataset.from_dict({"translation": transformed_validation_dataset})
        transformed_test = Dataset.from_dict({"translation": transformed_test_dataset})

        # Combine datasets into a DatasetDict
        transformed_datasets = DatasetDict({
            "train": transformed_train,
            "validation": transformed_validation,
            "test": transformed_test
        })

        tokenized_datasets = transformed_datasets.map(self.preprocess_function, batched=True)
        return tokenized_datasets

    def train_model(self, num_train_epochs=1, learning_rate=2e-5, weight_decay=0.01, batch_size=16):
        tokenized_datasets = self.load_and_prepare_datasets()

        data_collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.model, return_tensors="tf")

        train_dataset = self.model.prepare_tf_dataset(
            tokenized_datasets["train"],
            batch_size=batch_size,
            shuffle=True,
            collate_fn=data_collator,
        )

        validation_dataset = self.model.prepare_tf_dataset(
            tokenized_datasets["validation"],
            batch_size=batch_size,
            shuffle=False,
            collate_fn=data_collator,
        )

        optimizer = AdamWeightDecay(learning_rate=learning_rate, weight_decay_rate=weight_decay)
        self.model.compile(optimizer=optimizer)

        self.model.fit(train_dataset, validation_data=validation_dataset, epochs=num_train_epochs)

        self.model.save_pretrained("tf_model/")

    def translate_jap_to_eng(self, input_text):
        if self.model is None:
            raise ValueError("Model is not loaded or trained.")

        tokenized = self.tokenizer([input_text], return_tensors='np')
        out = self.model.generate(**tokenized, max_length=self.max_target_length)

        with self.tokenizer.as_target_tokenizer():
            eng_out = self.tokenizer.decode(out[0], skip_special_tokens=True)

        return eng_out

    def translate(self, text, model_name='Helsinki-NLP/opus-tatoeba-en-tr'):
        if not model_name:
            model_name = self.model_name

        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        encoded_text = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
        translated = model.generate(encoded_text)

        return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]



