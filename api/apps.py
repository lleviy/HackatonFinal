from django.apps import AppConfig
from django.conf import settings
import os
import pickle


class ApiConfig(AppConfig):
    path = os.path.join(settings.ML_MODELS, 'model.p')
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled)
    regressor = data['regressor']
    vectorizer = data['vectorizer']
