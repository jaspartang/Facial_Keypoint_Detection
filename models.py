## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        # floor((224-5)/1) + 1 = 220 --maxpooling(2,2)--> floor(110) = 110
        self.conv1 = nn.Conv2d(1, 32, 5) 
        self.conv1_bn = nn.BatchNorm2d(32)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        # floor((110-3)/1) + 1 = 108 --maxpooling(2,2)--> floor(54) = 54
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv2_bn = nn.BatchNorm2d(64)
        
        # floor((54-3)/1) + 1 = 52 --maxpooling(2,2)--> floor(26) = 26
        self.conv3 = nn.Conv2d(64, 128, 3)
        self.conv3_bn = nn.BatchNorm2d(128)
        
        # floor((26-2)/1) + 1 = 25 --maxpooling(2,2)--> floor(12.5) = 12
        self.conv4 = nn.Conv2d(128, 256, 2)
        self.conv4_bn = nn.BatchNorm2d(256)
        
        self.pool = nn.MaxPool2d(2, 2)
        
        # Now we flatten the output from the last convolutional layer which is 256 feature maps, each of size 12 x 12
        # when we flatten it into vector it becomes 12 * 12 * 256 = 36864 feature vector
        self.fc1 = nn.Linear(12*12*256, 2048)
        self.fc1_bn = nn.BatchNorm1d(2048)
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(2048, 512)
        self.fc2_bn = nn.BatchNorm1d(512)
        self.dropout2 = nn.Dropout(0.2)
        
        self.fc3 = nn.Linear(512, 136)
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        
        x = self.pool(F.relu(self.conv1_bn(self.conv1(x))))
        x = self.pool(F.relu(self.conv2_bn(self.conv2(x))))
        x = self.pool(F.relu(self.conv3_bn(self.conv3(x))))
        x = self.pool(F.relu(self.conv4_bn(self.conv4(x))))
        
        x = x.view(x.size(0),-1)
        
        x = self.dropout1(self.fc1_bn(F.relu(self.fc1(x))))
        x = self.dropout2(self.fc2_bn(F.relu(self.fc2(x))))
        x = self.fc3(x)
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
