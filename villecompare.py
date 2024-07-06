import difflib
import pandas as pd

df = pd.DataFrame([[1, 'Amsterdam'], [2, 'amsterdam'], [3, 'rotterdam'], [4, 'amstrdam'], [5, 'Berlin']])
df.columns = ['number', 'location']

df = df.loc[df.apply(lambda x: difflib.SequenceMatcher(None, 'Amsterdam', x.location).ratio() > 0.7, axis=1)]

print(df)
'''
df = pd.DataFrame([base_db])
df.columns = ['id', 'name']

df = df.loc[df.apply(lambda x: difflib.SequenceMatcher(None, name, x.location).ratio() > 0.7, axis=1)]

print(df)
'''
