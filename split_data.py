import os
import csv
import pandas as pd

df_good = pd.read_csv('.\\datasetcsv\\good.csv')
df_bad = pd.read_csv('.\\datasetcsv\\bad.csv')
good = df_good[df_good['Label']=='good']
bad = df_bad[df_bad['Label']=='bad']
#drop là xóa các index cũ, thay bằng index đánh số mới, inplace= true nghĩa là modify trên cái data frame đó luôn
#Nếu inplace=false là nó sẽ cho cái data frame mới.
good.reset_index(drop=True, inplace=True)
bad.reset_index(drop=True, inplace=True)
header = ['URL', 'Label']
# with open('.\\datasetcsv\\dataset_test\\bad.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)
path_predict = './datasetimg_test/bad'
for filename in os.listdir(path_predict):
    # print(filename)
    # print(filename.split("_"))
    haha = filename.split("_")
    # print(haha[1])
    hehe = haha[1].split(".")
    hehestr = str(hehe[0])
    # print(hehestr)
    line = bad['URL'][int(hehestr)]
    # print(line)
    arr_good = []
    arr_good.append([line, 'bad'])
    with open('.\datasetcsv\\dataset_test\\bad.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(arr_good)
    # print(hehe[0])
