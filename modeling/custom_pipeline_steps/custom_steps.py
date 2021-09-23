from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list):
        if not isinstance(columns, list):
            self.columns = [columns]
        else:
            self.columns = columns

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X[self.columns]
        return X


class ClipTransformer(TransformerMixin, BaseEstimator):
    
    def __init__(self, q = None):
      self.q_1 = None
      self.q_2 = None
      self.q = q

    def fit(self, X, y=None):
        if self.q is None: 
          self.q_1, self.q_2  = X.quantile(q = [0.1, 0.9])
        else: 
          self.q_1, self.q_2  = X.quantile(q = self.q)
        return self

    def transform(self, X):
        Xclip = np.array(np.clip(X, self.q_1, self.q_2)).reshape(-1, 1)
        return Xclip

class SingleSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]