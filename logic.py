import sys
import pandas as pd
from typing import List, Dict
from SPARQLWrapper import SPARQLWrapper, JSON
import cv2
from matplotlib import pyplot as plt
import os
import unicodedata
from PIL import Image

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
