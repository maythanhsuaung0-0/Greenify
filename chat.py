import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

# retrieve file and load the data
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]  # refer to the weights and biases of the model

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # ensures model behaves consistently when making predictions

bot_name = "Greeny"


# print("Let's chat! type 'quit' to exit")
# while True:
#     sentence = input("You: ")
#     if sentence == 'quit'.lower():
#         break

def get_response(msg):
    sentence = tokenize(msg)  # tokenize
    X = bag_of_words(sentence, all_words)  # bag_of_words
    # match expected input shape of neural network, reshape to have 1 row and equal to length of all_words
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)  # converted to PyTorch tensor, moved to device either GPU or CPU

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    # _ refer to max value on that dimension

    # retrieve corresponding tag
    tag = tags[predicted.item()]

    # check if probability of tag is high enough and then choose tag
    # softmax: convert raw output values into probabilities
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else:
        return "Sorry, I do not understand...Email us: enquiries@Greenify.com"



