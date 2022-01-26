import re
import numpy as np
import plotly.graph_objects as go
from nltk.util import ngrams, pad_sequence, everygrams
from nltk.tokenize import word_tokenize
from nltk.lm import MLE, WittenBellInterpolated


from scipy.ndimage import gaussian_filter

train_data_file = r'traindata_file.txt'

# read training data
with open(train_data_file, encoding='utf-8') as f:
    train_txt = f.read().lower()


# Formating text

train_txt = re.sub(r"\[.*\]|\{.*\}", "", train_txt)
train_txt = re.sub(r"[^\w\s]", "", train_txt)

# N-gran nubmer

n = 4

# tokenizing text

training_data = list(pad_sequence(word_tokenize(train_txt), n, pad_left=True, left_pad_symbol="<s>"))

# Generate N-Grams

ngrams = list(everygrams(training_data, max_len=n))
print('Number of ngrams:', len(ngrams))

# creating language models for n-grams

model = WittenBellInterpolated(n)
model.fit([ngrams], vocabulary_text=training_data)
print(model.vocab)

test_data_file = r'test_data_file_bad.txt'

# Read testing data

with open(test_data_file, encoding='utf-8') as f:
    test_txt = f.read().lower()

test_txt = re.sub(r'[^\w\s]', "", test_txt)

# tokenizing text

testing_data = list(pad_sequence(word_tokenize(test_txt), n, pad_left=True, left_pad_symbol="<s>"))
print(f'Test data size: {len(testing_data)}')

# Plagiasm scoring system

scores = []

for i, item in enumerate(testing_data[n-1:]):
    s = model.score(item, testing_data[i:i+n-1])
    scores.append(s)


scores_np = np.array(scores)

# seting boundaries
width = 8
height = np.ceil(len(testing_data)/width).astype("int32")
print(f'Width, Height: {width}, {height}')

# scores to array

a = np.zeros(width*height)
a[:len(scores_np)] = scores_np
result = len(a) - len(scores_np)

a = gaussian_filter(a, sigma=1.0)

a = a.reshape(-1, width)

# Labeling

labels = [' '.join(testing_data[i:i+width]) for i in range(n-1, len(testing_data), width)]
labels_individual = [x.split() for x in labels]
labels_individual[-1] += ['']*result

# Heatmaping

figure = go.Figure(data=go.Heatmap(
    z=a, x0=0, dx=1,
    y=labels, zmin=0, zmax=1,
    customdata=labels_individual,
    hovertemplate='%{customdata} <br><b>Score:%{z:.3f}<extra></extra>',
    colorscale='thermal'
))

figure.update_layout({'height':height*28, 'width':1000, 'font':{'family':'Arial'}})
figure['layout']['yaxis']['autorange'] = 'reversed'
figure.show()
