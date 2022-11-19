from src.dataloader import *
from src.log_and_visualization import *
from src.model import *
import time
import os
import argparse
import string
import gc
import keras.backend as K
from sklearn.utils import shuffle


def eval(g_model, d_model, gan_model, dataset, latent_dim, n_batch=32, savedir="dummy"):
    
    bat_per_epo = int(dataset[0].shape[0] / n_batch)

    dr1_hist, dr2_hist, df1_hist, df2_hist = list(), list(), list(), list()
    g_hist, gan_hist = list(), list()
    gan_acc_list = list()
    alphabet = string.ascii_lowercase + \
        string.digits + "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
    reverse_dictionary = {}
    for i, c in enumerate(alphabet):
        reverse_dictionary[i+1] = c
    
    b = 0
    start_time = time.time()

    for i in range(bat_per_epo):
        for j in range(2):
            d_model.trainable = False
            g_model.trainable = False
            
            [X_real, labels_real], y_real = generate_real_samples(
                dataset, i, n_batch)
            

            _, d_r1, d_r2 = d_model.test_on_batch(
                X_real, [y_real, labels_real])
            
            [X_fake, labels_fake], y_fake = generate_fake_samples(
                g_model, X_real, labels_real, latent_dim, n_batch)
            
            _, d_f1, d_f2 = d_model.test_on_batch(
                X_fake, [y_fake, labels_fake])
        
        d_model.trainable = False
        g_model.trainable = False
        
        z_input = generate_latent_points(latent_dim, n_batch)
        
        [X_real, labels_real], y_real = generate_real_samples(
            dataset, i, n_batch)
        g_loss = g_model.test_on_batch([X_real, z_input, labels_real], X_real)
        gan_loss, gan_cate_loss, gan_mse, _ ,gan_acc = gan_model.test_on_batch(
            [X_real, z_input, labels_real], [y_real, labels_real])
        
     
        print('>%d, dr[%.3f,%.3f], df[%.3f,%.3f], g[%.3f], gan[%.3f], gan_acc[%.3f]' % (
            i+1, d_r1, d_r2, d_f1, d_f2, g_loss, gan_loss, gan_acc))
        dr1_hist.append(d_r1)
        dr2_hist.append(d_r2)
        df1_hist.append(d_f1)
        df2_hist.append(d_f2)
        g_hist.append(g_loss)
        gan_hist.append(gan_loss)
        gan_acc_list.append(gan_acc)
        
    # summarize_performance_fixed(
    #     reverse_dictionary, b, g_model, d_model, dataset, 3, latent_dim, savedir=savedir)
    b = b + 1
    per_epoch_time = time.time()
    total_per_epoch_time = (per_epoch_time - start_time)/3600.0
    print(total_per_epoch_time)
    #summarize_performance(i, g_model, latent_dim,X_real,n_samples=n_batch,savedir=savedir)
    plot_history(dr1_hist, dr2_hist, df1_hist, df2_hist,
                 g_hist, gan_hist, savedir=savedir)
    to_csv(dr1_hist, dr2_hist, df1_hist, df2_hist,
           g_hist, gan_hist, savedir=savedir)
    print("Avg acc: ", np.mean(gan_acc_list))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--npz_file', type=str,
                        default='phishing.npz', help='path/to/npz/file')
    parser.add_argument('--latent_dim', type=int, default=50)
    parser.add_argument('--savedir', type=str, required=False,
                        help='path/to/save_directory', default='Haha')
    parser.add_argument('--weight_name_dis', type=str,
                        help='path/to/discriminator/weight/.h5 file', required=False)
    parser.add_argument('--weight_name_gen', type=str,
                        help='path/to/generator/weight/.h5 file', required=False)
    args = parser.parse_args()

    if not os.path.exists(args.savedir):
        os.makedirs(args.savedir)
    
    discriminator = define_discriminator()
 
    generator = define_generator(args.latent_dim)

    discriminator.load_weights("PhishGan/dmodel_000197.h5")
    generator.load_weights("PhishGan/gmodel_000197.h5")

    
    gan_model = define_gan(generator, discriminator)
   
    data = np.load(args.npz_file)
    dataset = shuffle(data['X_test'], data['y_test'])
   
    eval(generator, discriminator, gan_model, dataset,
         latent_dim=args.latent_dim, n_batch=args.batch_size, savedir=args.savedir)
