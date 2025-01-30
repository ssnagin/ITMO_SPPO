import pandas
import numpy
import matplotlib
import matplotlib.pyplot as plt

print("25 % 27 + 1 = " + str(25 % 27 + 1))

matplotlib.use('TkAgg')
csv_data = pandas.read_csv("mmycsv.csv").drop(["<TICKER>", "<PER>","<VOL>","<TIME>"], axis=1)

data = []

data.append(csv_data[csv_data["<DATE>"] == f"26/09/18"]["<OPEN>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/09/18"]["<HIGH>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/09/18"]["<LOW>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/09/18"]["<CLOSE>"])

data.append(csv_data[csv_data["<DATE>"] == f"26/10/18"]["<OPEN>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/10/18"]["<HIGH>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/10/18"]["<LOW>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/10/18"]["<CLOSE>"])

data.append(csv_data[csv_data["<DATE>"] == f"26/11/18"]["<OPEN>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/11/18"]["<HIGH>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/11/18"]["<LOW>"])
data.append(csv_data[csv_data["<DATE>"] == f"26/11/18"]["<CLOSE>"])

data.append(csv_data[csv_data["<DATE>"] == f"07/12/18"]["<OPEN>"])
data.append(csv_data[csv_data["<DATE>"] == f"07/12/18"]["<HIGH>"])
data.append(csv_data[csv_data["<DATE>"] == f"07/12/18"]["<LOW>"])
data.append(csv_data[csv_data["<DATE>"] == f"07/12/18"]["<CLOSE>"])


plt.figure(figsize=(10,5))
box=plt.boxplot(data, vert=True, patch_artist=True)

colors = plt.cm.get_cmap("coolwarm", 16)

for i, el in enumerate(box["boxes"]):
    el.set_facecolor(colors(i))

f = []
for i in ["09",'10','11','12']:
    fr = '26.'+i+'.2018'
    f+=[fr+' Открытие', fr + ' Макс', fr + ' Мин', fr + ' Закрытие']

plt.legend([box['boxes'][i] for i in range(16)],f, loc='upper left', frameon=False, bbox_to_anchor=(1, 1), ncol=1)

plt.tight_layout()
plt.show()