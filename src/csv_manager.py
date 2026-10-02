import pandas as pd
from datetime import datetime
import os


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)


CSV_FILE = os.path.join(PROJECT_ROOT, "history.csv")

data = pd.read_csv(CSV_FILE)



# CRUD operations

def get_all_history():

    return data



def save_submission(content_type, input_text, file_path, prediction):
    
    new_id = int(data['id'].max() + 1) if not data.empty else 1
    
    # id,content_type,input_text,file_path,prediction,timestamp
    new_row = {
        "id": new_id,
        "content_type": content_type,
        "input_text": input_text,
        "file_path": file_path,
        "prediction": prediction,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
    }
    
    new_data = pd.DataFrame([new_row])
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    
    return new_id


    
    
def delete_submission(id):
    
    if data.empty:
        return False
        
    target_row = data[data['id'] == int(id)]
    
    if target_row.empty:
        return False

    df_filtered = data[data['id'] != int(id)]

    df_filtered.to_csv(CSV_FILE, index=False)
    
    return True