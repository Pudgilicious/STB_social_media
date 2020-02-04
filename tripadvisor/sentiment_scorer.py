import pandas as pd
import traceback
from datetime import datetime
from pandas.io.json import json_normalize
from time import sleep

class SentimentScorer:
    def __init__(self, target_folder):
        self.target_folder = target_folder
