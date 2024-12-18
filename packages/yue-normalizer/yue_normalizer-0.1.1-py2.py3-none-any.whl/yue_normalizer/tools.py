import numpy as np
import matplotlib.pyplot as plt
import jiwer
# from camel_tools.tokenizers.word import simple_word_tokenize
import re
from pyarabic.araby import strip_tashkeel, normalize_ligature
from num2words import num2words
# from normalizer import BasicTextNormalizer
from .normalizer.normalizer import BasicTextNormalizer
import zhconv

basic_normalizer = BasicTextNormalizer()


def remove_chinese_punctuation_to_t(text):
    """
    移除汉语中常见的标点符号

    :param text: 输入的字符串
    :return: 移除标点后的字符串
    """
    # 定义汉语标点符号的正则表达式
    chinese_punctuation = r'[，。！？；：、“”‘’（）《》【】…—·]'
    # 使用正则表达式替换标点符号为空
    clean_text = re.sub(chinese_punctuation, '', text)
    clean_text = zhconv.convert(clean_text, 'zh-hk')
    return clean_text


def han_normalize(text, replace_space=True):
    text = basic_normalizer(text)
    if replace_space:
        return remove_chinese_punctuation_to_t(text).replace(' ', '')
    else:
        return remove_chinese_punctuation_to_t(text)
        


def normalize_arabic_text(text):
    # 去除标点和元音符号
    text = strip_tashkeel(text)
    
    # 规范化阿拉伯语字母连字
    text = normalize_ligature(text)
    
    # 将阿拉伯数字替换为标准数字
    arabic_to_digit = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3',
        '٤': '4', '٥': '5', '٦': '6', '٧': '7',
        '٨': '8', '٩': '9'
    }
    text = re.sub('|'.join(arabic_to_digit.keys()), lambda x: arabic_to_digit[x.group()], text)
    
    return text


def process_dataset(ds, model_id, language='arabic'):
    print('processing using language {}'.format(language))
    from transformers import WhisperFeatureExtractor
    from transformers import WhisperTokenizer
    tokenizer = WhisperTokenizer.from_pretrained(model_id, language=language, task="transcribe")
    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_id)
    
    def prepare_dataset(batch):
        try:
            # load and resample audio data from 48 to 16kHz
            audio = batch["audio"]
        
            # compute log-Mel input features from input audio array 
            batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features
        
            # encode target text to label ids 
            if "sentence" in batch:
                batch["labels"] = tokenizer(batch["sentence"]).input_ids
            elif 'text' in batch:
                batch["labels"] = tokenizer(batch["text"]).input_ids
            elif 'transcription' in batch:
                batch["labels"] = tokenizer(batch['transcription']).input_ids
            else:
                pass

            return batch
        except:
            batch["input_features"] = None
            batch["labels"] = None
            return batch
    
    ds = ds.map(prepare_dataset, num_proc=4)
    return ds


def arabic_preprocess(text):
    text = text[0]
    text = BasicTextNormalizer(True, False)(text)
    text = normalize_arabic_text(text)
    text = jiwer.RemovePunctuation()(text)  # 移除标点
    text = text.lower()
    words = simple_word_tokenize(text)
    rs_w = []
    for w in words:
        try:
            new_w = num2words(w, lang='ar')
        except:
            new_w = w
        rs_w.append(new_w)
    # print(rs_w)
    # print(len(rs_w))
    return [rs_w]


def plot_waveform(audio_array, sampling_rate):
    # Calculate the time axis in seconds
    time_axis = np.linspace(0, len(audio_array) / sampling_rate, num=len(audio_array))
    
    # Plot the waveform
    plt.figure(figsize=(15, 4))
    plt.plot(time_axis, audio_array, label="Audio Signal")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Waveform of the Audio Signal")
    plt.grid()
    plt.show()
