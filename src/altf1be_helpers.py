# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

from datetime import timedelta, datetime
from pathlib import Path
from os import path
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import glob
import sys
import re
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# constants
MISSING_LIBRARY = -1

# import libraries

class AltF1BeHelpers:

    @staticmethod
    def valid_time(string):
        """
            extract HH-MM-SS from a filename similar to /kaggle/input/2020-06-11_00-08-41-sca-tork-easycube-site.json
        """
        #print(f'string: {string}')
        try:
            mat=re.findall(r"([0-2][0-3]|[0-1][0-9])-([0-5][0-9])-([0-5][0-9])", string) # HH:MM:SS
            if mat is not None:
                    # print(f'mat: {"-".join(mat[1])}')
                    return ':'.join(mat[1])
            else:
                print('else')
                return None
        except ValueError:
            print("ValueError error:", sys.exc_info())
        print('None')
        return None

    @staticmethod
    def valid_date(string):
        """
            extract YYYY-MM-SS from a filename similar to /kaggle/input/2020-06-11_00-08-41-sca-tork-easycube-site.json
        """
        #print(f'string: {string}')
        try:
            mat=re.match(r'(?:(?:19|20)\d\d)-(?:11|12|10|0?[1-9])-(?:11|12|10|0?[1-9])', string) # YYY-MM-DD
            if mat is not None:
                #print(f'mat: {mat.group()}')
                return mat.group()
        except ValueError:
            print("ValueError error:", sys.exc_info())
        return None

    @staticmethod
    def count_files_in_dir(directory):
        
        def unique(list1): 
        
            # insert the list to the set 
            list_set = set(list1) 
            # convert the set to the list 
            unique_list = (list(list_set)) 
            for x in unique_list: 
                pass #print(x)
            return unique_list
        
        filenames = glob.glob(
            directory, 
            recursive=True
        )
        files_count = len(filenames)
        
        filenames_list = list()
        filenames_set = set()
        for filename in filenames:
            filenames_list.append(os.path.basename(filename))
            filenames_set.add(os.path.basename(filename))
            # print(f"os.path.basename(filename): {os.path.basename(filename)}")
        
        print(f"len(filenames_list): {len(filenames_list)}")
        print(f"len(filenames_set): {len(filenames_set)}")
        print(f"directory: {directory}")    
        print(f"files_count: {files_count}")
        
    @staticmethod
    def is_interactive():
        # return True if running on Kaggle
        try:
            return 'runtime' in get_ipython().config.IPKernelApp.connection_file
        except NameError:
            if (path.exists('/kaggle/working')):
                return True
            else:
                return False

    @staticmethod
    def unicode_to_ascii(a):
        """
        remove accents and apostrophes
        """
        try:
            import unidecode
        except ModuleNotFoundError:
            print(f"unidecode library is missing in you environment. Install unidecode or use conda or venv to set the right environment")
            exit(MISSING_LIBRARY)
        # def remove_accents_apostrophe(a):
        a = unidecode.unidecode(a)  # remove accent
        a = a.replace("'", '')  # remove apostrophe
        return a

    @staticmethod
    def input_directory(directories=[]) -> str:
        input_directory = '/kaggle/input'
        if AltF1BeHelpers.is_interactive():
            input_directory = os.path.join(
                input_directory, os.path.sep.join(directories))
        else:
            input_directory = os.path.join(os.path.abspath(
                os.getcwd()), "output_directory", "data", os.path.sep.join(directories))

        return input_directory

    @staticmethod
    def output_directory(directories=[]) -> str:
        output_directory = '/kaggle/working'
        if AltF1BeHelpers.is_interactive():
            output_directory = os.path.join(
                output_directory, os.path.sep.join(directories))
        else:
            output_directory = os.path.join(os.path.abspath(
                os.getcwd()), "output_directory", "data", os.path.sep.join(directories))

        Path(output_directory).mkdir(parents=True, exist_ok=True)
        return output_directory

    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


if __name__ == "__main__":

    text = "éè à iïî où &é'(§è!çàaQwxs $ µ `"
    print(
        f"unicode_to_ascii(text): '{text}' becomes '{AltF1BeHelpers.unicode_to_ascii(text)}'")
    print(f"is_interactive(): {AltF1BeHelpers.is_interactive()}")
    # print(f"output_directory(): {AltF1BeHelpers.output_directory(['delete_the_test_directory'])}")

    for single_date in AltF1BeHelpers.daterange(datetime.now() - timedelta(5), datetime.now() - timedelta(1)):
            #print(single_date.strftime("%Y-%m-%d"))
            print(f'daterange(): {single_date.strftime("%Y-%m-%d")}')
