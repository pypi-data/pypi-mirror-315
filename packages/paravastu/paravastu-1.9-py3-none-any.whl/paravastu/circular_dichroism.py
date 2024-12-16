import paravastu
import numpy as np
import pandas as pd

class circular_dichroism:
    def __init__(self, filenames):
        self.data = []
        for filename in filenames:
            df = pd.read_csv(filename, header=None)
            x = df.iloc[:, 0].values
            y = df.iloc[:, 1].values
            self.data.append(np.column_stack((x, y)))

    def find_min(self):
        minima = []
        for arr in self.data:
            min_idx = np.argmin(arr[:, 1])  # Find the index of the minimum y-value
            minima.append(tuple(arr[min_idx]))
        return minima

    def find_max(self):
        maxima = []
        for arr in self.data:
            max_idx = np.argmax(arr[:, 1])  # Find the index of the maximum y-value
            maxima.append(tuple(arr[max_idx]))
        return maxima
        
    def author():
        print("This class was developed by Anish Kelam")
