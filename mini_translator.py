from datasets import load_dataset, Dataset, DatasetDict
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, AdamWeightDecay, MarianMTModel, MarianTokenizer,DataCollatorForSeq2Seq
import tensorflow as tf
import re

import warnings

class MiniTranslator:
    def __init__(self):
        self.max_input_length = 128
        self.max_target_length = 128

        self.ja_to_en_model_name = "Helsinki-NLP/opus-mt-ja-en"
        self.ja_to_en_model_tokenizer = AutoTokenizer.from_pretrained(self.ja_to_en_model_name)
        self.ja_to_en_model = TFAutoModelForSeq2SeqLM.from_pretrained(self.ja_to_en_model_name)

        self.en_to_tr_model_name = "Helsinki-NLP/opus-tatoeba-en-tr"
        self.en_to_tr_model_tokenizer = AutoTokenizer.from_pretrained(self.en_to_tr_model_name)
        self.en_to_tr_model = TFAutoModelForSeq2SeqLM.from_pretrained(self.en_to_tr_model_name)

    def minitranslate(self,input):

        tokenized = self.ja_to_en_model_tokenizer(input, return_tensors='np')
        out = self.ja_to_en_model.generate(**tokenized, max_length=self.max_target_length)

        with self.ja_to_en_model_tokenizer.as_target_tokenizer():
            text = self.ja_to_en_model_tokenizer.decode(out[0], skip_special_tokens=True)

        tokenizer = MarianTokenizer.from_pretrained(self.en_to_tr_model_name)
        model = MarianMTModel.from_pretrained(self.en_to_tr_model_name)

        encoded_text = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
        translated = model.generate(encoded_text)

        return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

def list_to_srt(translated_lines):
    srt_content = ""
    entry_number = 1

    for line in translated_lines:
        if '-->' in line:
            srt_content += f"{entry_number}\n{line}\n"
            entry_number += 1
        else:
            srt_content += line + "\n"

    return srt_content


def translate_text(lines, option):
    for line in lines:

        time_stamp_pattern = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'

        if re.match(time_stamp_pattern, line.strip()):
            continue
        elif len(line.strip()) > 0:
            print("Orijinal:", line)

            if option == 'HIZLI':
                mini = MiniTranslator()
                translated_text = mini.minitranslate(line)

            else:
                print("Yavaş çeviri aracı şu anda kullanılamıyor.")
                # big = Translator()
                # translated_text = big.translate_jap_to_eng(line)
                # translated_text = big.translate(line)

            print("Çeviri:", translated_text)

            lines[lines.index(line)] = translated_text[0]
    return lines
