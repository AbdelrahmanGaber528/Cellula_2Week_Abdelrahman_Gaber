from pathlib import Path
import json
import torch
import pandas as pd
import numpy as np
from text_preprocessing import process_comment
from model import LSTM


def load_bundle(folder=None):
    
    if folder is None:
        folder = Path(__file__).resolve().parent.parent / "assets"
    else:
        folder = Path(folder)
        
    cfg = json.load(open(folder / "config.json", encoding="utf-8"))
    vocab = json.load(open(folder / "vocab.json", encoding="utf-8"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 
    model = LSTM(
        vocab_size=cfg["vocab_size"], 
        embedding_dim=cfg["embedding_dim"],
        hidden_dim=cfg["hidden_dim"], 
        num_layers=cfg["num_layers"],
        num_classes=cfg["num_classes"], 
        dropout=cfg.get("dropout", 0.3),
        bidirectional=cfg["bidirectional"],
    )
    
    state = torch.load(folder / "lstm_weights.pt", map_location=device)
    model.load_state_dict(state)
    model.to(device).eval()
    
    return model, vocab, cfg, device




def encode(texts, vocab, cfg, device):
    
    unk = vocab.get(cfg.get("unk_token", "<UNK>"), 1)
    max_len = cfg["max_len"]
    batch = []
    for t in texts:
        ids = [vocab.get(tok, unk) for tok in process_comment(str(t))][:max_len]
        ids += [0] * (max_len - len(ids))
        batch.append(ids)
        
    return torch.tensor(batch, dtype=torch.long, device=device)




@torch.no_grad()
def predict(texts, model, vocab, cfg, device, batch_size=64):
    
    labels = cfg["labels"]
    thresholds = cfg.get("thresholds", [0.5] * len(labels))
    out = []
    

    if isinstance(texts, str):
        texts = [texts]
        
    for i in range(0, len(texts), batch_size):
        x = encode(texts[i:i + batch_size], vocab, cfg, device)
        probs = torch.sigmoid(model(x)).cpu().numpy()
        out.append(probs)
        
    probs_df = pd.DataFrame(np.concatenate(out, axis=0), columns=labels)
    flags = probs_df.ge(pd.Series(thresholds, index=labels)).astype(int)
    
    return probs_df, flags