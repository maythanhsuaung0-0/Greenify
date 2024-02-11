import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

# tokenize + stem
all_words = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)  # append all tags in json file to array
    for pattern in intent['patterns']:
        w = tokenize(pattern)  # tokenize the pattern first; split into individual words into array
        all_words.extend(w)  # directly add w to all_words w/o the square brackets []
        xy.append((w, tag))  # use tuple: pattern, corresponding tag

# exclude punctuation characters + stemming
ignore_words = ['?', '!', '.', ',', '&', '#', '*', '(', ')', '+', '-']
all_words = [stem(w) for w in all_words if w not in ignore_words]  # stem the tokenized pattern + exclude punctuation

# sort: arrange alphabetically | set: remove duplicate elements in array
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# train data
x_train = []  # bag of words
y_train = []  # tag

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)  # CrossEntropyLoss

# convert into NumPy arrays; easier to work with machine learning when training dataset
x_train = np.array(x_train)
y_train = np.array(y_train)


# create training data
# inherit from parent: Dataset from PyTorch
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)  # number of str in array
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]  # returns a tuple containing the input data and its
        # corresponding label.

    def __len__(self):
        return self.n_samples


# Hyperparameters
num_epochs = 1000  # no. of times the entire dataset will be passed forward and backward during training
batch_size = 8  # no. if data samples processed in each min-batch
learning_rate = 0.001  # controls how much the model's parameters are updated
hidden_size = 18  # no, of neurons in hidden layer, trail and error
output_size = len(tags)
input_size = len(x_train[0])
print(input_size, len(all_words))
print(output_size, tags)


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss: determine how far off the predicted values are from actual, can adjust model parameters to make it more accurate
criterion = nn.CrossEntropyLoss()

# Optimizer: adjust lr for each parameter to minimize loss
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device).long()

        # Forward pass
        outputs = model(words)  # predictions
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)  # compare with predictions and actual tags

        # Backward and optimize
        optimizer.zero_grad()  # set gradient to 0 for parameters
        loss.backward()  # calculates how much each model parameter contributed to the error
        optimizer.step()  # update parameters to reduce loss

    # check if current epoch is multiple of 100 and to see periodic updates on training progress
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

# save the model as dict
data = {
    "model_state": model.state_dict(),  # saving current state of the model's parameters  
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f"training complete, file saved to {FILE}")
