
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import warnings
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta
warnings.filterwarnings('ignore')

import numpy as np
from scipy import linalg
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm
from sklearn import model_selection
from sklearn.metrics import accuracy_score






df = pd.read_csv('dataset.csv', header=0, sep=',', index_col=False)

df_filter = df[['date','people', 'empoyed', 'capita_income', 'capita_expenses',
                 'nom_wages_company','GNP', 'prod_fossils',
                 'prod_energy_water_gas', 'agriculture_flower',
                 'area_house', 'retail', 'energy']]
#df_filter = df_filter.query('date>= "2018-12-27 00:00:00"')
min_date = pd.to_datetime(df_filter['date'].max(), format='%Y.%m.%d %H:%M:%S') + timedelta(hours=1)
loc = 0

date = []
people = []
empoyed = []
capita_income = []
capita_expenses = []
nom_wages_company = []
GNP = []
fixed_assets = []
prod_fossils = []
prod_energy_water_gas = []
agriculture_flower = []
area_house = []
retail = []
energy = []
interval = 24*61


for i in range(interval):
    date.append(min_date)
    min_date = min_date + timedelta(hours=1)
    loc += 1
for name in list(df_filter):
    if name != 'date':
        dataset_total = df_filter[['date', name]]
        len_dataset = int(len(dataset_total)*0.80)
        train_total = dataset_total[:len_dataset]
        test_total = dataset_total[len_dataset:]

        train_total.index = train_total['date']
        train_total = train_total[name]
        test_total.index = test_total['date']
        test_total = test_total[name]
        train_values = train_total.values
        test_values = test_total.values

        predictions = list()
        history = []
        for x in train_values:
            history.append(x)
        for y in range(len(test_values)+interval):
            model = sm.tsa.SARIMAX(history, order=(0,1,0), seasonal_order=(1,0,0,12),enforce_stationarity=False)
            #ARIMA(history, order=(7, 0, 1))
            model = model.fit(disp=0)
            forecast = model.forecast(steps=interval)
            yhat = int(forecast[0])
            predictions.append(yhat)
            if y < len(test_values):
                obs = test_values[y]
            else:
                obs = yhat
                if name == 'people':
                    people.append(yhat)
                if name == 'empoyed':
                    empoyed.append(yhat)
                if name == 'capita_income':
                    capita_income.append(yhat)
                if name == 'capita_expenses':
                    capita_expenses.append(yhat)
                if name == 'nom_wages_company':
                    nom_wages_company.append(yhat)
                if name == 'GNP':
                    GNP.append(yhat)
                if name == 'prod_fossils':
                    prod_fossils.append(yhat)
                if name == 'prod_energy_water_gas':
                    prod_energy_water_gas.append(yhat)
                if name == 'agriculture_flower':
                    agriculture_flower.append(yhat)
                if name == 'area_house':
                    area_house.append(yhat)
                if name == 'retail':
                    retail.append(yhat)
                if name == 'energy':
                    energy.append(yhat)
            history.append(obs)
        print(test_values, '\n' ,predictions[:-2])
        print(accuracy_score(test_values, predictions[:-2],normalize=False))

        def my_custom_loss_func(y_true, y_pred):
            diff = np.abs(y_true/y_pred).max()
            return np.log1p(diff)
        print(my_custom_loss_func(test_values,predictions[:-2]))


d = {'people': people, 'empoyed': empoyed, 'capita_income': capita_income, 'capita_expenses': capita_expenses, 'nom_wages_company': nom_wages_company,
     'GNP': GNP, 'prod_fossils':prod_fossils, 'prod_energy_water_gas': prod_energy_water_gas, 'agriculture_flower': agriculture_flower,
     'area_house': area_house, 'retail': retail}

pred = pd.DataFrame(data=d)
print(pred)

x_trn = df_filter.loc[:, ('people', 'empoyed', 'capita_income', 'capita_expenses', 'nom_wages_company', 'GNP',
                          'prod_fossils', 'prod_energy_water_gas', 'agriculture_flower', 'area_house', 'retail')]
y_trn = df_filter.loc[:, 'energy']
x_train, x_test, y_train, y_test = train_test_split(x_trn, y_trn, test_size=0.2)
model = LinearRegression().fit(x_train, y_train)
model.predict(x_test)
y_pred_futere = model.predict(pred)
pred['date'] = date
pred['energy'] = y_pred_futere
#print(pred)
pred.to_csv('predictions.csv', header=True)

