import requests
import json
from zipfile import ZipFile
import torch



import os
from getpass import getpass
import urllib

import nltk
nltk.download('punkt')   
      
    
    
squad_url_train = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json'
squad_url_dev = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json'
squad_filepath_train = 'SQuAD_train_v1.1.json'
squad_filepath_dev = 'SQuAD_dev_v1.1.json'

    
fasttext_url='https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip'
fasttext_zipfilepath='fastText/crawl-300d-2M.vec.zip'
fasttext_drectory='fastText'

    
infersent_git='facebookresearch/InferSent.git'
infersent_url='https://dl.fbaipublicfiles.com/infersent/infersent2.pkl'
infersent_filepath='infersent/infersent2.pkl'




def download(url,filePath):
    with open(filePath, 'wb') as f:
        f.write(requests.get(url).content)

def download_squad():

    download(squad_url_train,squad_filepath_train)
    download(squad_url_dev,squad_filepath_dev)


def collect_squad_data():

    with open(squad_filepath_train) as f:
        return json.load(f)
    
    
def download_fasttext():
    download(urlFastText,zipFilePathFastText)
    
   
    with ZipFile(zipFilePathFastText, 'r') as f:
        f.extractall(filePathFastText)
    

class Credentials():
    def __enter__(self):
        print("Please enter github credentials:")
        return {"user":input('User name: '),"password":urllib.parse.quote(getpass('Password: '))}

    def __exit__(self, exc_type, exc_val, exc_tb):
        return
    
    
def download_infersent():
    with Credentials() as creds:
        os.system('git clone https://{0}:{1}@github.com/{2} master'.format(creds["user"],creds["password"],infersent_git))
    
    download(infersent_url,infersent_filepath)
    

def build_infersent_model(use_cuda = True, vocab_size=1e5):
    from models import InferSent

    params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                    'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}
    model = InferSent(params_model)
    model.load_state_dict(torch.load(infersent_filepath))
    
    
    model = model.cuda() if use_cuda else model
    model.set_w2v_path('fastText/crawl-300d-2M.vec')
    
    model.build_vocab_k_words(K=vocab_size)
    
    return model