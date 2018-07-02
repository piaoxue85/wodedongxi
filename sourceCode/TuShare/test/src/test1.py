import numpy as np
import pandas as pd

df = pd.DataFrame()
df["a"] = [2,2,2,2,2]
df["b"] = [2,2,2,2,2]
df["c"] = [3,3,3,3,3]
df["d"] = df["c"].values * (df["a"].values/df["b"].values)

print(df)