import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results.csv')
plt.bar(df['Algorithm'], df['Total Lateness'])
plt.title('EDF verus SJF Performance')
plt.xlabel('Algorithm')
plt.ylabel('Total Lateness (hours)')
plt.savefig('edf_vs_sjf_performance.png')