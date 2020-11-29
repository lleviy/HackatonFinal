from django.apps import AppConfig
from django.conf import settings
import os
import pickle
import numpy


class ApiConfig(AppConfig):
    path = os.path.join(settings.ML_MODELS, 'scores_energy.pickle')
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled)
    # regressor = data['regressor']
    # vectorizer = data['vectorizer']

    energy_predictions = data['XGBoost']
    # выработка электроэнергии на 6 месяцев вперед


