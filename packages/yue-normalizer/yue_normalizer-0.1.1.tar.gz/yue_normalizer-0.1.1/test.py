from yue_normalizer.tools import han_normalize
from yue_normalizer.chinese_normalizer import TextNorm

text_norm = TextNorm(remove_fillers=True, remove_space=True)
print(text_norm("奧利佛‧薩克斯在他的文章〈總統的演講〉中，指出因為腦部受損而無法理解演講內容的人，仍然可以準確感受到演講者的誠意。"))
