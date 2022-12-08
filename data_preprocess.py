import pandas as pd
import keras
from keras.preprocessing.text import Tokenizer 
import string
import numpy as np
from keras.utils import to_categorical
import argparse
import matplotlib.pyplot as plt
import csv
import os 

def tokenizer(alphabet,url_length=200):
    dictionary_size = len(alphabet) + 1
    url_shape = (url_length, dictionary_size)
    dictionary = {}
    reverse_dictionary = {}
    for i, c in enumerate(alphabet):
        dictionary[c]=i+1
        reverse_dictionary[i+1]=c
    return dictionary, reverse_dictionary
    
def data_npz(good,bad,alphabet,dictionary,samples=50000,url_length=200,npz_filename='phishing.npz'):
        #Good hay Bad data gì đi nữa thì nó sẽ cho vào cái mảng 200x67
        good_data = []   
        i = 0
        # i_good = 0
        # header = ['URL', 'Label']
        # arr_good = [] 
        for i in range(20):
            line = good['URL'][i]
            this_sample=np.zeros(url_shape)
            # if(line[0] == "'" and line[-1] == "'"):
            #     line = line[1:-1]
            # line = line.replace("'","%27")
            # line = line.replace(" ","%20")    
            line = line.lower()
            # for i, position in enumerate(this_sample):
            #     this_sample[i][0]=1.0
            # for i, char in enumerate(line):
            #     this_sample[i][0]=0.0
            #     this_sample[i][dictionary[char]]=1.0
            # good_data.append(this_sample)    
            if len ( set(line) - set(alphabet)) == 0 and len(line) < args.url_length and line.find('.') != -1:
                #print(i)
                for i, position in enumerate(this_sample):
                    this_sample[i][0]=1.0

                for i, char in enumerate(line):
                    this_sample[i][0]=0.0
                    this_sample[i][dictionary[char]]=1.0
                plt.imshow(this_sample, cmap='gray')
                dirgood = ".\\datasetimg\\good\\" + "GOOD_" + str(i_good) + ".png"
                plt.imsave(dirgood, this_sample)
                good_data.append(this_sample)
                i_good = i_good + 1
                # arr_good.append([line, 'good'])
            else:
                print("Uncompatible line:", line)
            
        # with open('.\\datasetcsv\\good.csv', 'w', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(header)
        #     writer.writerows(arr_good)
        #print("Data ready. Lines:", len(good_data))
        good_data = np.array(good_data)
        # good_data = good_data[:samples]
        print ("Done Good")

        bad_data = []   
        i = 0
        # i_bad = 0
        # arr_bad = []  
        for i in range(20):
            line = bad['URL'][i]
            this_sample=np.zeros(url_shape)
            # if(line[0] == "'" and line[-1] == "'"):
            #     line = line[1:-1]
            # line = line.replace("'","%27")
            # line = line.replace(" ","%20")
            line = line.lower()
            for i, position in enumerate(this_sample):
                this_sample[i][0]=1.0
            for i, char in enumerate(line):
                this_sample[i][0]=0.0
                this_sample[i][dictionary[char]]=1.0            
            bad_data.append(this_sample)
            # if len ( set(line) - set(alphabet)) == 0 and len(line) < args.url_length and line.find('.') != -1:
            #     for i, position in enumerate(this_sample):
            #         this_sample[i][0]=1.0

            #     for i, char in enumerate(line):
            #         this_sample[i][0]=0.0
            #         this_sample[i][dictionary[char]]=1.0
            #     # plt.imshow(this_sample, cmap='gray')
            #     # dirbad = ".\\datasetimg\\bad\\" + "BAD_" + str(i_bad) + ".png"
            #     # plt.imsave(dirbad, this_sample)
            #     bad_data.append(this_sample)
                # i_bad = i_bad + 1
                # arr_bad.append([line, 'bad'])
            # else:
            #     print("Uncompatible line:",  line)
            
        # with open('.\\datasetcsv\\bad.csv', 'w', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(header)
        #     writer.writerows(arr_bad)
        #print("Data ready. Lines:", len(bad_data))
        bad_data = np.array(bad_data)
        # bad_data = bad_data[:samples]
        print("--------------------------------------------------------")
        print ("Array Shape:", good_data.shape)
        print ("Array Shape:", bad_data.shape)
        # x_train_len = int(samples* 0.8)
        #good_data và bad_data giờ đây là mảng 3 chiều, dùng kĩ thuật slicing và indexing.
        #số luong x dòng x cột, nên mới có :x_train_len,:,: nghĩa là dòng và cột lấy hết còn số lượng lấy từ đầu đến 80%
        #axis=0 thì nó cho bad_data append sau thằng good_data.
        x_train = np.concatenate((good_data[:18,:,:], bad_data[:18,:,:]),axis=0)
        x_test = np.concatenate((good_data[18:20,:,:], bad_data[18:20,:,:]),axis=0)
        #Đánh nhãn cho các samples good_Data và bad_data
        good_label = np.ones((20,1))
        bad_label = np.zeros((20,1))
        #to_categorical là chuyển các số thành dạng binary, ở đây là label chỉ có 2 nhãn là 0 và 1.
        # Chuyển 0 và 1 ra nhị phân (dạng mặc định của to_categorical là float32)
        y_train = np.concatenate((good_label[:18,:], bad_label[:18,:]),axis=0)        
        y_train_cat = to_categorical(y_train)
        y_test = np.concatenate((good_label[18:20,:], bad_label[18:20,:]),axis=0)
        y_test_cat = to_categorical(y_test)

        np.savez_compressed(npz_filename, X_train=x_train, X_test=x_test, y_train=y_train_cat, y_test=y_test_cat)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--url_length', type=int, default=200)
    parser.add_argument('--npz_filename', type=str, default='phishing_2_2.npz')
    parser.add_argument('--n_samples',type=int, default=140000,help='number of good and bad samples.')
    args = parser.parse_args()

    
    alphabet = string.ascii_lowercase + string.digits + "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
    dictionary_size = len(alphabet) + 1
    url_shape = (args.url_length, dictionary_size)
    
    #392923 GOOD, 156420 BAD
    # df = pd.read_csv('phishing_site_urls.csv')
    df_good = pd.read_csv('.\\datasetcsv\\good.csv')
    df_bad = pd.read_csv('.\\datasetcsv\\bad.csv')
    # good = df[df['Label']=='good']
    # bad = df[df['Label']=='bad']
    good = df_good[df_good['Label']=='good']
    bad = df_bad[df_bad['Label']=='bad']
    
    #drop là xóa các index cũ, thay bằng index đánh số mới, inplace= true nghĩa là modify trên cái data frame đó luôn
    #Nếu inplace=false là nó sẽ cho cái data frame mới.
    good.reset_index(drop=True, inplace=True)
    bad.reset_index(drop=True, inplace=True)

    # rows_good = good[good.columns[0]].count()
    # rows_bad = bad[bad.columns[0]].count()
    # print("Good: ", rows_good, " ==== Bad: " ,rows_bad)
    # Good:  392924  ==== Bad:  156422

    each_class_samples= args.n_samples #2
    dictionary, reverse_dictionary = tokenizer(alphabet,url_length= args.url_length)

    # if not os.path.exists(".\\datasetimg\\good"):
    #     os.makedirs(".\\datasetimg\\good")
    # if not os.path.exists(".\\datasetimg\\bad"):
    #     os.makedirs(".\\datasetimg\\bad")
    data_npz(good,bad,alphabet,dictionary,samples=each_class_samples,url_length=args.url_length,npz_filename=args.npz_filename)

    

