import unicodedata
import pandas as pd
from PIL import Image
import datetime
import numpy as np
from collections import OrderedDict


FOLDER_PATH="raw_data/output_imdb_top100/"

class DataRetrieval:

    def get_celeb_image(name_):
        name_wo_diacritics = ''.join(c for c in unicodedata.normalize('NFD',name_)
                  if unicodedata.category(c) != 'Mn')
        celeb_image_file = "_".join(name_wo_diacritics.lower().split())+".jpg"
        image_path = FOLDER_PATH+celeb_image_file
        image = Image.open(f"{image_path}")
        return image


    def get_data_celebrities():
        return pd.read_csv("raw_data/list_act.csv")

    def celeb_selector(mode='daily', test_index=0, file_path='raw_data/metafile_complete.csv'):

        selection_df = pd.read_csv(file_path)

        # Standard mode
        if mode=='daily':
            np.random.seed(int(datetime.date.today().strftime(r'%d%m%Y')))
            celeb_index = np.random.choice(selection_df.shape[0])

        # For testing we can choose any celebrity index
        elif mode == 'test':
            celeb_index = test_index

        # Otherwise random every time
        else:
            celeb_index = np.random.choice(selection_df.shape[0])

        hidden_celebrity = selection_df['Celebrity'].iloc[celeb_index]
        hint_items = selection_df.iloc[:,2:].iloc[celeb_index].tolist()
        hint_titles = selection_df.iloc[:,2:].columns
        hint = {k:v for k,v in zip(hint_titles, hint_items)}

        # Ordering hints
        hint = OrderedDict(hint)
        key_order= ['Gender', 'Occupation', 'Citizenship', 'Age']
        for k in key_order:
            hint.move_to_end(k)

        return hidden_celebrity , hint, selection_df

    def celeb_and_score_query(selected_celebrity, hidden_celebrity, names_df, score_df):
        celeb_rank = names_df[hidden_celebrity][names_df[hidden_celebrity] == selected_celebrity].index
        celeb_score = score_df[hidden_celebrity].loc[celeb_rank].iloc[0]
        return selected_celebrity, celeb_score
