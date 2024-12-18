from tqdm.auto import tqdm
import time
import pandas as pd
import warnings
from ..preprocessing._utils.tools import to_df
from ..forecaster import get_result

warnings.filterwarnings('ignore')

MODELS = [
    "prophet", "lstnet", "lstm", "bilstm", "convlstm", 
    "tcn", "rnn", "arima", "sarima"
]

class Timeseries:
    def __init__(self, dataFrame: pd.DataFrame, y: str, dateColumn: str, forecastingStartDate: str, 
                 models: str = "all", epoch: int = 2, metrics: str = "mape", process: bool = False, 
                 forecastNumber: int = 24):

        self.dataFrame = dataFrame
        self.y = y
        self.dateColumn = dateColumn
        self.models = models
        self.process = process
        self.epoch = epoch
        self.forecastNumber = forecastNumber
        self.forecastingStartDate = forecastingStartDate
        self.metrics = metrics

    def fit(self):
        if not isinstance(self.dataFrame, pd.DataFrame) or self.dataFrame.empty:
            raise ValueError('Data is empty or not a DataFrame.')

        if self.models == "all":
            self.models = MODELS.copy()
        else:
            if isinstance(self.models, list):
                self.models = [model.lower().strip() for model in self.models]
                valid_models = [model for model in self.models if model in MODELS]
                if not valid_models:
                    raise ValueError("Invalid Model(s) provided.")
                self.models = valid_models
            else:
                raise TypeError("models must be a list or 'all'.")

        names, metrics_ = [], []
        for model in tqdm(self.models):
            start = time.time()
            try:
                forecast, evaluate = get_result(
                    dataFrame=self.dataFrame, y=self.y, modelName=model, metric=self.metrics,
                    dateColumn=self.dateColumn, process=self.process, forecastNumber=self.forecastNumber,
                    epoch=self.epoch, forecastingStartDate=self.forecastingStartDate
                )
                names.append(model)
                metrics_.append(evaluate)
            except Exception as e:
                print(f"Error with model {model}: {e}")

        predictions = pd.DataFrame()
        for m, n in zip(metrics_, names):
            if len(self.metrics) == 1:
                predictions = pd.concat([predictions, to_df(data=m.split(":")[1], index=[n], columns=[m.split(":")[0]])])
            else:
                predictions = pd.concat([predictions, to_df(m, [n])])

        return predictions
