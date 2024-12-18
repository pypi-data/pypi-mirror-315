from prophet import Prophet
import logging
from datetime import datetime as dt
from perlib.core.tester import dTester
from typing import Union,List
import pickle
import os
import pandas as pd

class ProphetModel:

    def __init__(self, dfnow, n_test_hours,
                 datetime_test_start,freq,
                 col_y, col_ds,metric: Union[str, List[str]] = "mape",cols_feat=None,future_periods=24
                 ):

        self.dfnow = dfnow
        self.freq = freq
        self.n_test_hours = n_test_hours
        self.datetime_test_start = datetime_test_start
        self.col_y = col_y
        self.col_ds = col_ds
        self.cols_feat = cols_feat
        self.metric = metric
        self.future_periods = future_periods
        

        self.dfnow = self.dfnow.rename({self.col_ds: 'ds', self.col_y: 'y'}, axis=1)

        self.df_test = self.dfnow[self.dfnow['ds']>=self.datetime_test_start].copy()
        self.df_test = self.df_test.set_index('ds', drop=False)
        self.df_test['yhat'] = None

        self.test_len_hours = (self.dfnow.ds.max() - datetime_test_start).total_seconds() / 60 / 60
        self.n_test_steps = int(self.test_len_hours // self.n_test_hours)

        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
        if self.cols_feat:
            for col_feat in self.cols_feat:
                self.model.add_regressor(col_feat)

        self.step = 0

    def train(self):
        
        logging.info(f"Training with data up to test_start: {self.datetime_test_start}")
        
        df_train = self.dfnow[self.dfnow.ds<self.datetime_test_start]
        
        logging.info(f"Start: {df_train.ds.min()}, End: {df_train.ds.max()}, # of hours: {df_train.shape[0]}")

        self.model.fit(df_train)

        logging.info(f"Finished training.")

    def step_without_train(self):

        datetime_thr = self.datetime_test_start + dt.timedelta(hours=self.n_test_hours*self.step)
        df_test = self.dfnow[(self.dfnow.ds>=datetime_thr) & (self.dfnow.ds<datetime_thr+dt.timedelta(hours=self.n_test_hours))]

        forecast = self.model.predict(df_test)

        self.step += 1

    def step_with_train(self):

        datetime_thr = self.datetime_test_start + dt.timedelta(hours=self.n_test_hours*self.step)
        df_train = self.dfnow[self.dfnow.ds<datetime_thr]
        df_test = self.dfnow[(self.dfnow.ds>=datetime_thr) & (self.dfnow.ds<datetime_thr+dt.timedelta(hours=self.n_test_hours))]

        self.model.fit(df_train)

        forecast = self.model.predict(df_test)

        self.step += 1

    def update_result(self, forecast):

        forecast = forecast.set_index('ds', drop=False)
        
        self.df_test.update(forecast['yhat'])

    #def get_mape_results(self):
    #    logging.info("Getting MAPE results")
#
    #    # Copy to avoid modifying the original dataframe
    #    df_test_copy = self.df_test.copy()
    #    df_test_copy.loc[df_test_copy.y == 0, 'y'] = 1
    #    df_test_copy.loc[df_test_copy.y < 1, 'y'] = 1
#
    #    # Calculate MAPE
    #    df_test_copy['Mape'] = np.abs((df_test_copy.y - df_test_copy.yhat) / df_test_copy.y)
#
    #    # Determine the time difference between rows to adapt to data frequency
    #    time_diff = df_test_copy.ds.diff().min()
#
    #    # Compute the number of intervals for slicing
    #    n_intervals = int((self.df_test.ds.max() - self.datetime_test_start) / time_diff)
#
    #    # Results DataFrame
    #    df_results = pd.DataFrame(columns=['Interval_Start', 'Interval_End', 'MAPE'])
#
    #    for interval in range(0, n_intervals, self.n_test_steps):
    #        interval_start = self.df_test.ds.min() + interval * time_diff
    #        interval_end = interval_start + (self.n_test_steps - 1) * time_diff
#
    #        # Filter df_test_copy for the current interval
    #        interval_data = df_test_copy[(df_test_copy.ds >= interval_start) & (df_test_copy.ds <= interval_end)]
#
    #        # Calculate mean MAPE for the interval
    #        mean_mape = interval_data.Mape.mean()
#
    #        # Append results
    #        df_results = df_results.append({
    #            'Interval_Start': interval_start, 
    #            'Interval_End': interval_end, 
    #            'MAPE': mean_mape
    #        }, ignore_index=True)

    #    return df_results
    
    def get_mape_results(self):
        
        logging.info(f"Getting Mape results")

        n_zeros = (self.df_test.y == 0).sum()
        if n_zeros>0:
            logging.warning(f"{n_zeros} values in the test data are zero! Converting to 1")
            self.df_test[self.df_test.y==0, 'y'] = 1

        n_smalls = (self.df_test.y < 1).sum()
        if n_smalls > 0:
            logging.warning(f"{n_smalls} values are smaller than zero! Converting to 1")
            self.df_test[self.df_test.y<1, 'y'] = 1

        self.df_test['Mape'] = np.abs(self.df_test.y - self.df_test.yhat) / self.df_test.y

        slice_starts = [self.df_test.iloc[0].name + dt.timedelta(hours=shift) 
                        for shift in range(0, self.df_test.shape[0], self.n_test_hours) ]

        slice_ends = [startnow + dt.timedelta(hours=self.n_test_hours-1) for startnow in slice_starts]

        df_result = pd.DataFrame(data={'Start': slice_starts, 'End': slice_ends})
        df_result['Mape'] = None

        for ii in range(self.n_test_hours):
            df_result['Hour' + str(ii).zfill(2)] = None

        for indnow, (startnow, endnow) in enumerate(zip(slice_starts, slice_ends)):
            
            dftmp = self.df_test.loc[startnow:endnow]
            
            mapenow = dftmp.Mape.mean()
            
            for ii in range(self.n_test_hours):
                df_result.loc[indnow, 'Hour' + str(ii).zfill(2)] = dftmp.iloc[ii].Mape
            
            df_result.loc[indnow,'Mape'] = mapenow

        return df_result


    def validate_singletrain(self):
        prefix="models/"
        model_name = f'Data-Prophet-{dt.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        logging.info("Validation using single training")
        
        self.train()
        
        df_test = self.dfnow[self.dfnow['ds'] > self.datetime_test_start].copy()

        directory = os.path.dirname(prefix + model_name + '.pkl')
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True) 

        with open(prefix + model_name + '.pkl', 'wb') as file:
            pickle.dump(self.model, file)
        print(f"Model saved as {prefix + model_name + '.pkl'}")

        if not df_test.empty:
            logging.info("Forecasting test data with existing test set")
            forecast = self.model.predict(df_test)
            self.forecast = forecast
            df_test['ds'] = pd.to_datetime(df_test['ds'])
            forecast['ds'] = pd.to_datetime(forecast['ds'])
            forecast = pd.merge(df_test[['ds', 'y']], forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')
            forecast.rename(columns={'y': 'actual'}, inplace=True)
            if 'actual' in forecast.columns:
                calc = dTester.calculate(Yhat=forecast['yhat'].values, actual=forecast['actual'].values, metric=self.metric)
            else:
                calc = "Actual values not provided; unable to calculate performance metrics."
        else:
            logging.info("Test data is empty; checking for future predictions with additional regressors.")
            if self.cols_feat is None:
                future = self.model.make_future_dataframe(periods=self.future_periods+1,freq=self.freq)
                future = future[future['ds'] > self.datetime_test_start]
                forecast = self.model.predict(future)
                self.forecast = forecast
                forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
                calc = f"Forecasted {self.future_periods} days into the future."
            else:
                logging.info("Unable to forecast future data with additional regressors due to missing future values.")
                forecast = None
                calc = "No test data and missing future values for additional regressors."

        return forecast, calc

        #df_result = self.get_mape_results()

        #logging.info(f"Finished! Mape-mean: {df_result.Mape.mean()}, Mape-std: {df_result.Mape.std()}")
    
    def make_future_predictions(self, model_or_path, testData):
        """
        Accepts the model as a file path or directly as a model object.
        Predicts the future and returns the results.
        
        :param model_or_path: Trained Prophet model or file path where the model is saved
        :param testData: DataFrame with future dates and values of additional regressors
        :return: DataFrame with prediction results
        """
        if isinstance(model_or_path, str):
            # Eğer model_or_path bir string ise, bir dosya yoludur ve modeli yüklememiz gerekir
            try:
                with open(model_or_path, 'rb') as file:
                    model = pickle.load(file)
            except FileNotFoundError:
                raise FileNotFoundError(f"Model file not found at {model_or_path}")
        elif isinstance(model_or_path, Prophet):
            # Eğer model_or_path bir Prophet model nesnesi ise, doğrudan kullanabiliriz
            model = model_or_path
        else:
            raise ValueError("model_or_path must be a Prophet model instance or a path to a pickle file containing a Prophet model.")

        forecast = model.predict(testData)
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        return forecast
