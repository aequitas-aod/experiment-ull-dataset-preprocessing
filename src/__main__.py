import os

import pandas as pd

from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
)
from src.pre_processing.principal_questionnaire import preprocess_principal_questionnaire


def main():

    print(preprocess_principal_questionnaire())


if __name__ == "__main__":
    main()
