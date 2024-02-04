import torch.nn as nn
import torch.nn.functional as F


# inheritance, inherits from parent: nn.Module - base class for all PyTorch neural network modules
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNet, self).__init__()
        #  apply linear transformation on its input using a weight matrix and bias to produce output
        # input size: size of input data provided
        self.l1 = nn.Linear(input_size, hidden_size)

        # hidden size: size of intermediate tensor produced by each linear layer
        self.l2 = nn.Linear(hidden_size, hidden_size)

        # output size: size of final output tensor
        self.l3 = nn.Linear(hidden_size, output_size)

    # forward method: forward pass of the neural network
    def forward(self, x):
        out = F.relu(self.l1(x))
        out = F.relu(self.l2(out))
        out = self.l3(out)
        return out  # final output tensor

    # activation function: neurons are responsible for making decisions in this area
    # Rectified Linear Unit ReLu: only +ve values allowed to flow through function, if -ve, map to 0
