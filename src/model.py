import torch.nn as nn
import torch


class LSTM(nn.Module):
    
    def __init__(
        self,
        vocab_size,
        embedding_dim=128,
        hidden_dim=128,
        num_layers=2,
        num_classes=6,
        dropout=0.3,
        bidirectional=False
    ):
        
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
            padding_idx=0
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=bidirectional
        )

        direction = 2 if bidirectional else 1

        self.fc = nn.Linear(
            hidden_dim * direction,
            num_classes
        )

    def forward(self, x):
        
        x = self.embedding(x)

        output, (hidden, cell) = self.lstm(x)

        if self.lstm.bidirectional:
            hidden = torch.cat(
                (hidden[-2], hidden[-1]),
                dim=1
            )
        else:
            hidden = hidden[-1]

        return self.fc(hidden)