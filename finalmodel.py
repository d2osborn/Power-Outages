import pandas as pd
import numpy as np
import plotly.io as pio
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
import datetime

pio.renderers.default = 'notebook'
pd.options.plotting.backend = 'plotly'

from dsc80_utils import *

outage = pd.read_excel('outage.xlsx')
outage = outage.iloc[4:, 1:]
outage = outage.reset_index(drop=True)
outage.columns = outage.iloc[0]
outage = outage.iloc[2:, :]
outage = outage.reset_index(drop=True)

def change_to_time(date, time):
    combined = pd.to_datetime(date[date.notna()].astype(str) + ' ' + time[time.notna()].astype(str), 
                              errors='coerce')
    return combined

outage['OUTAGE.START'] = change_to_time(outage['OUTAGE.START.DATE'], outage['OUTAGE.START.TIME'])
outage['OUTAGE.RESTORATION'] = change_to_time(outage['OUTAGE.RESTORATION.DATE'], 
                                              outage['OUTAGE.RESTORATION.TIME'])

outage = outage.drop(columns=['OUTAGE.START.DATE','OUTAGE.START.TIME','OUTAGE.RESTORATION.DATE',
                              'OUTAGE.RESTORATION.TIME'])

datetime_cols = ['OUTAGE.START', 'OUTAGE.RESTORATION']

str_cols = ['U.S._STATE', 'POSTAL.CODE', 'NERC.REGION', 
            'CLIMATE.REGION', 'CLIMATE.CATEGORY', 'CAUSE.CATEGORY', 
            'CAUSE.CATEGORY.DETAIL', 'HURRICANE.NAMES']
outage[str_cols] = outage[str_cols].astype('string')

int_cols = ['OBS', 'YEAR', 'OUTAGE.DURATION', 
            'DEMAND.LOSS.MW', 'CUSTOMERS.AFFECTED', 'RES.SALES', 
            'COM.SALES', 'IND.SALES', 'TOTAL.SALES', 
            'RES.CUSTOMERS', 'COM.CUSTOMERS', 'IND.CUSTOMERS', 
            'TOTAL.CUSTOMERS', 'PC.REALGSP.STATE', 'PC.REALGSP.USA', 
            'UTIL.REALGSP', 'TOTAL.REALGSP', 'POPULATION']
outage[int_cols] = outage[int_cols].astype('Int64')

float_cols = [col for col in outage.columns if col not in str_cols and col not in int_cols 
              and col not in datetime_cols]
outage[float_cols] = outage[float_cols].astype('Float64')

outage[['OUTAGE.DURATION', 
        'DEMAND.LOSS.MW', 
        'CUSTOMERS.AFFECTED']] = outage[['OUTAGE.DURATION', 'DEMAND.LOSS.MW', 
                                         'CUSTOMERS.AFFECTED']].replace(0, np.nan)

outage = outage.applymap(lambda x: np.nan if pd.isnull(x) else x)

sunrise = datetime.time(6, 0, 0)
sunset = datetime.time(20, 0, 0)
outage['IS_DARK'] = np.where(outage['OUTAGE.START'].isnull(), np.nan, 
                             (outage['OUTAGE.START'].dt.time >= sunset) | 
                             (outage['OUTAGE.START'].dt.time <= sunrise))

outage = outage.drop(columns=['CAUSE.CATEGORY.DETAIL', 'HURRICANE.NAMES'])

outage = outage[(outage['U.S._STATE'] != 'Hawaii') & (outage['U.S._STATE'] != 'Alaska')]

# MAR columns
# Categorical
outage['MONTH'] = outage['MONTH'].fillna(7.0)
outage['CLIMATE.REGION'] = outage['CLIMATE.REGION'].fillna(outage['CLIMATE.REGION'].mode())
outage['CLIMATE.CATEGORY'] = outage['CLIMATE.REGION'].fillna(outage['CLIMATE.REGION'].mode())
outage['OUTAGE.START'] = outage['OUTAGE.START'].ffill()
outage['OUTAGE.RESTORATION'] = outage['OUTAGE.RESTORATION'].ffill()
outage['IS_DARK'] = np.where(outage['OUTAGE.START'].isnull(), np.nan, 
                             (outage['OUTAGE.START'].dt.time >= sunset) | 
                             (outage['OUTAGE.START'].dt.time <= sunrise))

# Numeric
def prob_impute(s):
    s = s.copy()
    num_null = s.isna().sum()
    fill_values = np.random.choice(s.dropna(), num_null)
    s[s.isna()] = fill_values
    return s


numerical = ['RES.PRICE', 'COM.PRICE', 'IND.PRICE', 'TOTAL.PRICE', 'RES.SALES', 'COM.SALES', 'IND.SALES', 
             'TOTAL.SALES', 'RES.PERCEN', 'COM.PERCEN', 'IND.PERCEN', 'POPDEN_UC', 'POPDEN_RURAL']

outage['OUTAGE.DURATION'] = (outage.groupby('CAUSE.CATEGORY')['OUTAGE.DURATION'].transform(prob_impute))
for i in numerical:
    outage[i] = (outage.groupby('CLIMATE.CATEGORY')[i].transform(prob_impute))


# MCAR columns
def quantitative_distribution(data):
    values = []
    bins = []
    hist, bin_edges = np.histogram(data.dropna())
    hist = hist / len(data.dropna())
    for i in range(len(bin_edges) - 1):
        bins.append(bin_edges[i:i + 2])
    for i in range(len(data) - data.count()):
        selected_bin = bins[np.random.choice(len(bins), p=hist)]
        values.append(np.random.uniform(selected_bin[0], selected_bin[1]))
    return np.array(values)

def impute_quantitative_column(column_data):
    missing_values = column_data.isnull()
    distribution = quantitative_distribution(column_data)
    column_data[missing_values] = distribution[:sum(missing_values)]
    return column_data

outage['ANOMALY.LEVEL'] = impute_quantitative_column(outage['ANOMALY.LEVEL'])
outage['DEMAND.LOSS.MW'] = impute_quantitative_column(outage['DEMAND.LOSS.MW'])
outage['CUSTOMERS.AFFECTED'] = impute_quantitative_column(outage['CUSTOMERS.AFFECTED'])

outage['POP.DENSITY.URBAN'] = outage['POPULATION'] / outage['AREAPCT_URBAN']
outage['AVG.MONTHLY.PRICE'] = outage[['RES.PRICE', 'COM.PRICE', 'IND.PRICE']].mean(axis=1)

features = ['CLIMATE.REGION', 'PC.REALGSP.STATE', 'YEAR', 'MONTH', 'NERC.REGION', 
            'POPULATION', 'PCT_WATER_INLAND', 'POSTAL.CODE', 'POP.DENSITY.URBAN', 
            'AVG.MONTHLY.PRICE']
target = 'TOTAL.SALES'
X = outage[features]
y = outage[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['POPULATION', 'PCT_WATER_INLAND', 'PC.REALGSP.STATE', 
                                   'POP.DENSITY.URBAN', 'AVG.MONTHLY.PRICE']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['CLIMATE.REGION', 'POSTAL.CODE', 'NERC.REGION'])
    ], remainder='passthrough')
model = RandomForestRegressor()
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])
params = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 20, None]
}
grid_search = GridSearchCV(pipeline, params, cv=5, scoring='r2', n_jobs=-1, verbose=10, 
                           error_score='raise')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
best_model.fit(X, y)

y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
r2