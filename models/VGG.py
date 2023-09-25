from modules.model import LitModel
import torch.nn as nn



config = {
    '11': [64, 'P', 128, 'P', 256, 256, 'P', 512, 512, 'P', 512, 512, 'P'],
    '13': [64, 64, 'P', 128, 128, 'P', 256, 256, 'P', 512, 512, 'P', 512, 512, 'P'],
    '16': [64, 64, 'P', 128, 128, 'P', 256, 256, 256, 'P', 512, 512, 512, 'P', 512, 512, 512, 'P'],
    '19': [64, 64, 'P', 128, 128, 'P', 256, 256, 256, 256, 'P', 512, 512, 512, 512, 'P', 512, 512, 512, 512, 'P'],
}



class VGG(LitModel):
    def __init__(
            self, 
            version: int, 
            num_classes: int,
            hidden_features: int = 512, 
            dropout: float = 0.5
        ):
        super().__init__()
        self.num_classes = num_classes
        self.features = self._construction(version)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512*7*7, hidden_features),
            nn.ReLU(True),
            nn.Dropout(dropout),
            nn.Linear(hidden_features, hidden_features),
            nn.ReLU(True),
            nn.Dropout(dropout),
            nn.Linear(hidden_features, num_classes)
        )


    def _construction(self, name):
        sequence = nn.Sequential()
        in_channels = 3
        for x in config[name]:
            if x == 'P':
                sequence.extend([
                    nn.MaxPool2d(kernel_size=2, stride=2)
                ])
            else:
                sequence.extend([
                    nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
                    nn.BatchNorm2d(x),
                    nn.ReLU(True)
                ])
                in_channels = x
        return sequence


    def forward(self, x):
        out = self.features(x)
        out = self.classifier(out)
        return out



class VGG11(VGG):
    def __init__(self, num_classes: int, hidden_features: int = 512, dropout: float = 0.5):
        super().__init__("11", num_classes, hidden_features, dropout)



class VGG13(VGG):
    def __init__(self, num_classes: int, hidden_features: int = 512, dropout: float = 0.5):
        super().__init__("13", num_classes, hidden_features, dropout)



class VGG16(VGG):
    def __init__(self, num_classes: int, hidden_features: int = 512, dropout: float = 0.5):
        super().__init__("16", num_classes, hidden_features, dropout)



class VGG19(VGG):
    def __init__(self, num_classes: int, hidden_features: int = 512, dropout: float = 0.5):
        super().__init__("19", num_classes, hidden_features, dropout)
