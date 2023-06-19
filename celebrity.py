import unicodedata
import pandas as pd
from PIL import Image
import datetime
import numpy as np


FOLDER_PATH="raw_data/output_imdb_top100/"

class DataRetrieve:

    def get_image(name_):
        name_no_accents = ''.join(c for c in unicodedata.normalize('NFD',name_)
                  if unicodedata.category(c) != 'Mn')
        person_name = "_".join(name_no_accents.lower().split())+".jpg"
        image_path = FOLDER_PATH+person_name
        image = Image.open(f"{image_path}")
        return image



    def get_data_celebrities():
        return pd.read_csv("raw_data/list_act.csv")

    def celeb_selector(mode='daily', test_index=0, file_path='metafile.csv'):

        selection_df = pd.read_csv(file_path)
        selection_df = selection_df.iloc[:,1:].drop(columns=['item','image'])

        def birth_date_to_age(birth_date):
            birth_date  = birth_date[:10]
            birth_date = datetime.datetime.strptime(birth_date, r'%Y-%m-%d').date()
            today = datetime.date.today()
            age = today.year - birth_date.year
            full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
            if not full_year_passed:
                age -= 1
            return age

        selection_df['bdayLabel'] = selection_df['bdayLabel'].apply(lambda x: x[:10])
        selection_df['age'] = selection_df['bdayLabel'].apply(birth_date_to_age)


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

        hidden_celebrity = selection_df['itemLabel'].iloc[celeb_index]
        hint = selection_df.iloc[:,1:].iloc[celeb_index].tolist()

        return hidden_celebrity , hint

    def celeb_and_score_query(celebrity, hidden_celebrity, names_df, score_df):
        celeb_rank = names_df[hidden_celebrity][names_df[hidden_celebrity] == celebrity].index
        celeb_score = score_df[hidden_celebrity].loc[celeb_rank].iloc[0]
        return celebrity, celeb_score
