import torch
import yfinance as yf
import joblib

from torch import nn

class AcaoModel(nn.Module):
    def __init__(self, input_size:int, hidden_size:int, num_layers:int, output_size:int):
        super(AcaoModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x:torch.tensor):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(DEVICE)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(DEVICE)
        x = x.to(DEVICE)
        out, _ = self.rnn(x, (h0, c0))
        out = self.fc(out[:, -1, :])

        return SCALER.inverse_transform(out.detach().cpu().squeeze().numpy().reshape(-1, 1))
    
    @staticmethod
    def load(device:torch.device):
        net = AcaoModel(1, 5, 1, 1).to(device)
        net.load_state_dict(torch.load('app/models/stock_rnn.pth', map_location=device))
        return net

def obter_dados_acao_preparados(ticker:str):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1mo')[-22:-1]
    close = data['Close'].values.reshape(-1, 1)
    close = SCALER.transform(close)
    return torch.tensor(close).float().unsqueeze(0), data.index[-1]


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SCALER = joblib.load('app/models/stock_rnn_scaler.pkl')
MODEL = AcaoModel.load(DEVICE)
