from torch import nn
import torch.nn.functional as F


class LeNet(nn.Module):
    def __init__(self, dropout_mode: str, dropout_rate: float):
        super().__init__()
        self.fc0 = nn.Linear(28 * 28, 300)
        self.fc1 = nn.Linear(300, 100)
        self.fc2 = nn.Linear(100, 10)
        
        if dropout_mode == '0d':
            self.dropout = nn.Dropout(dropout_rate)
        elif dropout_mode == '1d':
            self.dropout = nn.Dropout1d(dropout_rate)
        else:
            raise ValueError('invalid value for dropout mode')
    
    def forward(self, x):
        x = F.relu(self.fc0(x))
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def get_activation_hook(act, idx):
    def hook(model, input, output):
        act[idx] = output.detach().numpy()
    return hook


def add_hooks(model):
    act = [None for _ in range(2)]
    handles = [
        model.fc0.register_forward_hook(get_activation_hook(act, 0)),
        model.fc1.register_forward_hook(get_activation_hook(act, 1)),
    ]
    return act, handles


def remove_hooks(handles):
    for handle in handles:
        handle.remove()


def get_activations(model, data):
    act, handles = add_hooks(model)
    _ = model(data)
    remove_hooks(handles)
    return act