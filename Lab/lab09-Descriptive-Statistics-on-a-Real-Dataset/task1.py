import seaborn as sns
import pandas as pd

pd.set_option('display.width', 120)
df = sns.load_dataset('tips')

print('SHAPE:', df.shape)
print('\nINFO:')
df.info()
print('\nDESCRIBE:\n', df.describe())
