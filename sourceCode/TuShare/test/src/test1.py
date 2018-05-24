import numpy as np
import pandas as pd

np1 = np.array([1,2])
np2 = np.array([2,2])
data = pd.DataFrame(np1+np2,columns=["aa"]).sort_values("aa",ascending =False)
print(data)
