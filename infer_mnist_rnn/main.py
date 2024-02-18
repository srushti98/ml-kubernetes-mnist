import gradio as gr
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import torch.nn as nn
from PIL import Image
import io

# Your existing Net class here
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.rnn = nn.LSTM(input_size=28, hidden_size=64, batch_first=True)
        self.batchnorm = nn.BatchNorm1d(64)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(64, 32)
        self.fc2 = nn.Linear(32, 10)

    def forward(self, input):
        # Shape of input is (batch_size,1, 28, 28)
        # converting shape of input to (batch_size, 28, 28)
        # as required by RNN when batch_first is set True
        input = input.reshape(-1, 28, 28)
        output, hidden = self.rnn(input)

        # RNN output shape is (seq_len, batch, input_size)
        # Get last output of RNN
        output = output[:, -1, :]
        output = self.batchnorm(output)
        output = self.dropout1(output)
        output = self.fc1(output)
        output = F.relu(output)
        output = self.dropout2(output)
        output = self.fc2(output)
        output = F.log_softmax(output, dim=1)
        return output

def predict(image):
    image = Image.fromarray(image).convert('L')

    # Transform the image to the format expected by the network
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # Apply transformation
    image = transform(image).unsqueeze(0)

    # Load model and set to eval mode
    model = Net()
    model.load_state_dict(torch.load("/model/mnist_rnn.pt", map_location=torch.device('cpu')))
    print("Model loaded successfully")
    model.eval()

    # Make prediction
    with torch.no_grad():
        output = model(image)
        predicted = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability

    return predicted.item()

# Define Gradio interface
iface = gr.Interface(fn=predict,
                     inputs=gr.Image(),
                     outputs="text",
                     title="MNIST Digit Recognition",
                     description="Upload an image of a digit to see its MNIST classification")

if __name__ == "__main__":
    iface.launch()
