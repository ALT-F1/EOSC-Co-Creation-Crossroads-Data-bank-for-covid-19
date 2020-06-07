# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

from pathlib import PurePath

from altf1be_helpers import AltF1BeHelpers

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


class BPost_postal_codes():
    """ 
        The class provides a read-to-use dataframe to manipulate the postal codes 
        made available by the Belgian postal office
    """

    def initialize_variables(self):
        self.altF1BeHelpers = AltF1BeHelpers()

        # source https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal
        postal_codes_in_be_from_bpost_be_in_fr_path = "kaggle/input/bpost-postal-codes/zipcodes_alpha_fr_new.csv"

        # source https://www.bpost.be/site/nl/verzenden/adressering/zoek-een-postcode
        postal_codes_in_be_from_bpost_be_in_nl_path = "kaggle/input/bpost-postal-codes/zipcodes_alpha_nl_new.csv"

        if (self.altF1BeHelpers.is_interactive()):
            self.postal_codes_in_be_from_bpost_be_in_fr_path = f"/{postal_codes_in_be_from_bpost_be_in_fr_path}"
            self.postal_codes_in_be_from_bpost_be_in_nl_path = f"/{postal_codes_in_be_from_bpost_be_in_nl_path}"
        else:
            # source https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal
            self.postal_codes_in_be_from_bpost_be_in_fr_path = os.path.join(
                os.path.abspath(os.getcwd()),
                "src",
                postal_codes_in_be_from_bpost_be_in_fr_path
            )

            # source https://www.bpost.be/site/nl/verzenden/adressering/zoek-een-postcode
            self.postal_codes_in_be_from_bpost_be_in_nl_path = os.path.join(
                os.path.abspath(os.getcwd()),
                "src",
                postal_codes_in_be_from_bpost_be_in_nl_path
            )

        self.missing_english_cities = pd.DataFrame(
            {"Code postal": [1000, 1342, 7941, 1060, 6238, 8300, 4850],
                "Localité": ["Brussels", "Ottignies", "Chasse Royale", "Cureghem", "Brunehault", "Knokke-Heist", "Plombières"],
                "Commune principale": ["Brussels", "Ottignies", "BRUGELETTE", "SAINT-GILLES", "PONT-À-CELLES", "KNOKKE-HEIST", "Plombières"],
                "Province": ["BRUXELLES", "BRABANT WALLON", "HAINAUT", "BRUXELLES", "HAINAUT", "FLANDRE-OCCIDENTALE", "LIEGE"]
             }
        )

    def get_postal_codes(self):
        """
            Extract the Belgian postal codes from the BPOST.BE database
        """
        # source https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal
        columns = {
            'Postcode': 'Code postal',
            'Plaatsnaam':  'Localité',
            'Deelgemeente': 'Sous-commune',
            'Hoofdgemeente': 'Commune principale',
            'Provincie': 'Province'
        }
        self.postal_codes_in_be_from_bpost_be_in_fr = pd.read_csv(
            self.postal_codes_in_be_from_bpost_be_in_fr_path,
            sep=',',
            header=0
        )
        self.postal_codes_in_be_from_bpost_be_in_nl = pd.read_csv(
            self.postal_codes_in_be_from_bpost_be_in_nl_path,
            sep=',',
            header=0
        )

        # rename the columns in NL to facilitate the concatenation
        self.postal_codes_in_be_from_bpost_be_in_nl = self.postal_codes_in_be_from_bpost_be_in_nl.rename(
            columns=columns,
            errors='raise'
        )

        df = pd.concat([
            self.postal_codes_in_be_from_bpost_be_in_nl,
            self.postal_codes_in_be_from_bpost_be_in_fr
        ])

        return df

    def remove_non_existing_cities(self, df):
        df = df.drop(df[df['Code postal'] == 612].index)

        return df

    def keep_certain_columns_in_df(self, df):
        """
        Reduce the amount of columns in final self.df_postal_codes_in_be
        """

        # keep fewer columns
        df = df[
            ['Code postal', 'Commune principale', 'Localité', 'Province']
        ]

        return df

    def add_missing_names_in_en(self, df):
        """
        Transform: Add missing names in English in BPOST database
        """

        # add missing cities
        df = df.append(
            self.missing_english_cities
        )

        return df

    def columns_in_lowercase(self, df):
        """        
        Transform: change columns in lower case
        """
        # change column to lowercase
        df['Localité'] = df['Localité'].str.lower(
        )
        df['Commune principale'] = df['Commune principale'].str.lower(
        )

        return df

    def remove_non_ascii_characters(self, df):
        """
        Transform: remove accents and apostophes and use 'normalized' columns
        """
        df['Commune principale normalized'] = df['Commune principale'].apply(
            self.altF1BeHelpers.unicode_to_ascii
        )

        df['Localité normalized'] = df['Localité'].apply(
            self.altF1BeHelpers.unicode_to_ascii
        )

        return df

    def drop_duplicates(self, df):
        """
        Transform: drop all duplicates from self.df_postal_codes_in_be
        """

        # drop duplicates and keep the first one
        df = df.drop_duplicates(
            keep='first')

        return df

    def save(self, df):
        save_file_in = os.path.join(
            self.altF1BeHelpers.output_directory(['BPost.be']), "df_postal_codes_in_be.xlsx")

        print(f"Save DataFrame in '{save_file_in}'")

        df.to_excel(save_file_in)

    def __init__(self):
        self.initialize_variables()
        self.df_postal_codes_in_be = self.get_postal_codes()
        self.df_postal_codes_in_be = self.remove_non_existing_cities(
            self.df_postal_codes_in_be)
        self.df_postal_codes_in_be = self.keep_certain_columns_in_df(
            self.df_postal_codes_in_be)
        self.df_postal_codes_in_be = self.add_missing_names_in_en(
            self.df_postal_codes_in_be)
        self.df_postal_codes_in_be = self.columns_in_lowercase(
            self.df_postal_codes_in_be)
        self.df_postal_codes_in_be = self.remove_non_ascii_characters(
            self.df_postal_codes_in_be)
        self.df_postal_codes_in_be = self.drop_duplicates(
            self.df_postal_codes_in_be)
        self.save(self.df_postal_codes_in_be)


if __name__ == "__main__":
    bpost_postal_codes = BPost_postal_codes()
    print(
        f"is_interactive() : {bpost_postal_codes.altF1BeHelpers.is_interactive()}")

    print(bpost_postal_codes.df_postal_codes_in_be)
