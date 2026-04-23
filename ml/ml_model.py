from sklearn.linear_model import LogisticRegression
import numpy as np

def train_model():
    X = np.array([
        [180,170],
        [150,160],
        [200,180],
        [140,150]
    ])

    y = np.array([1,0,1,0])

    model = LogisticRegression()
    model.fit(X,y)

    return model
