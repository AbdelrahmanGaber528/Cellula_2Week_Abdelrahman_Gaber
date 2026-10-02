from .predict import load_bundle, predict


_model, _vocab, _cfg, _device = load_bundle()

print("LSTM model loaded successfully!")


def classify_text(text):

    if not text or not str(text).strip():
        return []
        

    _, flags = predict([text], _model, _vocab, _cfg, _device)
    
    row = flags.iloc[0]
    detected_labels = [label for label, val in row.items() if val == 1]
    
    return detected_labels