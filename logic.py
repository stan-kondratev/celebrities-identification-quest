import sys
import pandas as pd
from typing import List, Dict
from SPARQLWrapper import SPARQLWrapper, JSON
import cv2
from matplotlib import pyplot as plt
import os
import unicodedata
from PIL import Image
import numpy as np
import datetime

folder_path = "raw_data/output_imdb_top100/"

class WikiDataQueryResults:
    """
    A class that can be used to query data from Wikidata using SPARQL and return the results as a Pandas DataFrame or a list
    of values for a specific key.
    """
    def __init__(self, query: str):
        """
        Initializes the WikiDataQueryResults object with a SPARQL query string.
        :param query: A SPARQL query string.
        """
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

    def __transform2dicts(self, results: List[Dict]) -> List[Dict]:
        """
        Helper function to transform SPARQL query results into a list of dictionaries.
        :param results: A list of query results returned by SPARQLWrapper.
        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        new_results = []
        for result in results:
            new_result = {}
            for key in result:
                new_result[key] = result[key]['value']
            new_results.append(new_result)
        return new_results

    def _load(self) -> List[Dict]:
        """
        Helper function that loads the data from Wikidata using the SPARQLWrapper library, and transforms the results into
        a list of dictionaries.
        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        results = self.sparql.queryAndConvert()['results']['bindings']
        results = self.__transform2dicts(results)
        return results

    def load_as_dataframe(self) -> pd.DataFrame:
        """
        Executes the SPARQL query and returns the results as a Pandas DataFrame.
        :return: A Pandas DataFrame representing the query results.
        """
        results = self._load()
        return pd.DataFrame.from_dict(results)


class DataRetrieve:
    def show_imgs(img1,img2, folder_path):

        # create figure
        fig = plt.figure(figsize=(10, 7))

        # setting values to rows and column variables
        rows = 1
        columns = 2



        img1_path = folder_path+img1
        img2_path = folder_path+img2


        # reading images
        Image1 = cv2.imread(img1_path)
        Image2 = cv2.imread(img2_path)

        RGB_img1 = cv2.cvtColor(Image1, cv2.COLOR_BGR2RGB)
        RGB_img2 = cv2.cvtColor(Image2, cv2.COLOR_BGR2RGB)

        # Adds a subplot at the 1st position
        fig.add_subplot(rows, columns, 1)

        # showing image
        plt.imshow(RGB_img1)
        plt.axis('off')
        plt.title("First")

        # Adds a subplot at the 2nd position
        fig.add_subplot(rows, columns, 2)

        # showing image
        plt.imshow(RGB_img2)
        plt.axis('off')
        plt.title("Second")

    def get_image(name_):
        name_no_accents = ''.join(c for c in unicodedata.normalize('NFD',name_)
                  if unicodedata.category(c) != 'Mn')
        person_name = "_".join(name_no_accents.lower().split())+".jpg"
        image_path = folder_path+person_name
        image = Image.open(f"{image_path}")
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
