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

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# constants
MISSING_LIBRARY = -1

# import libraries


def is_interactive():
    # return True if running on Kaggle
    try:
        return 'runtime' in get_ipython().config.IPKernelApp.connection_file
    except NameError:
        if (path.exists('/kaggle/working')):
            return True
        else:
            return False


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


def output_directory(directories):
    output_directory = '/kaggle/working'
    if is_interactive():
        output_directory = os.path.join(
            output_directory, ','.join(directories))
    else:
        output_directory = os.path.join(os.path.abspath(
            os.getcwd()), "output_directory", "data", ','.join(directories))

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    return output_directory

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == "__main__":
    text = "éè à iïî où &é'(§è!çàaQwxs $ µ `"
    print(
        f"unicode_to_ascii(text): '{text}' becomes '{unicode_to_ascii(text)}'")
    print(f"is_interactive(): {is_interactive()}")
    print(f"output_directory(): {output_directory(['new_directory'])}")

    for single_date in daterange(datetime.now() - timedelta(5), datetime.now() - timedelta(1)):
            #print(single_date.strftime("%Y-%m-%d"))
            print(f'daterange(): {single_date.strftime("%Y-%m-%d")}')

