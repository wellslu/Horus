# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
@gitHub: https://github.com/aaron1aaron2
@Create Date: 2021/1/5
"""
import re
import os
import glob
import time 
import json
import argparse
import itertools
import numpy as np
import pandas as pd

import cv2
from torch.backends import cudnn

from .utils import get_data
from .predict.fastreid.config import get_cfg
from .predict.predictor import FeatureExtractionDemo

cudnn.benchmark = True

__all__ = ["ReidMatch"]

class ReidMatch(FeatureExtractionDemo):
    def __init__(self, model_file, example_img, parallel=False):
        """
        Args:
            model_file (str): pretrain folder, Must contain `config.yaml` and `model_final.pth` under folder.
            parallel (bool): whether to run the model in different processes from visualization.

        Functions:
            run_on_image: Use the pre-trained model to convert the input image(`original_image`)
                          into feature vectors(shape: (1, 2048)). (Inherited from class `FeatureExtractionDemo`)

            cosine_similarity: Calculate the cosine similarity between vector `a` and vector `b`

            match_folders_under_path: 

            match_two_folder: 

            get_features:

            image_to_feature

        """
        self.config_file = os.path.join(model_file, "config.yaml")
        self.model_file = os.path.join(model_file, "model_final.pth")
        self.parallel = parallel

        self._check_data(model_file)
        self.cfg = self._set_config()
        super(ReidMatch, self).__init__(self.cfg, parallel)
        self._warm_up_model(example_img)



    def match_two_folder(self, f1, f2, output_folder, sample_nums, sim_threshold, sup_threshold, sample_in_bin,
                         same_folder=False, save_feature=True, result_output=None, result_table_output=None):
        for path in [f1, f2]:
            assert os.path.exists(path), "Can't find folder at {}".format(path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        START_time = time.time()
        result = {"Args":{"f1":f1, "f2":f2, "output_folder":output_folder, "sample_nums":sample_nums,
                        "sim_threshold":sim_threshold, "sup_threshold":sup_threshold, "same_folder":same_folder,
                        "save_feature":save_feature, "result_output":result_output, 
                        "result_table_output":result_table_output
                            },
                  "Path":{},
                  "Time":{},
                  "Result":{}
                        }
        
        # Sampling
        print("\nSampling...")
        imgs_in_f1 = self._get_random_item(input_ls=os.listdir(f1), size=sample_nums, sample_in_bin=sample_in_bin)
        imgs_in_f2 = self._get_random_item(input_ls=os.listdir(f2), size=sample_nums, sample_in_bin=sample_in_bin)
        print("samples in folder1: {}".format(imgs_in_f1))
        print("samples in folder2: {}".format(imgs_in_f2))

        imgs_in_f1 = [(1, os.path.join(f1, file)) for file in imgs_in_f1]
        imgs_in_f2 = [(2, os.path.join(f2, file)) for file in imgs_in_f2]
        result["Path"].update({"f1_sample_paths":[path for _,path in imgs_in_f1]})
        result["Path"].update({"f2_sample_paths":[path for _,path in imgs_in_f2]})

        imgs = imgs_in_f1 + imgs_in_f2
        df = pd.DataFrame(imgs)
        df.columns = ["folder", "img_path"]

        # Extracting features
        print("\nExtracting features...")
        start_time = time.time()
        feat_paths, feats = self.get_features(
                                    paths=df['img_path'].to_list(), 
                                    output_folder=output_folder,
                                    save_feature=save_feature
                                    )
        df['feature'] = feats
        df['feature_path'] = feat_paths
        result["Path"].update({"f1_feature_paths":df.loc[df['folder']==1, 'feature_path'].to_list()})
        result["Path"].update({"f2_feature_paths":df.loc[df['folder']==2, 'feature_path'].to_list()})
        result["Time"].update({"extracting_features_timeuse":time.time() - start_time})
        print("time use: ", result["Time"]["extracting_features_timeuse"])

        # Pairing image
        pair_df = pd.DataFrame(list(itertools.combinations(df['img_path'], 2)))
        pair_df.columns = ["img1", "img2"]

        # Calculate similarity
        print("\nCalculate similarity...")
        start_time = time.time()
        path_folder_dt = {v:(k, f, fp) for k,v,f,fp in df.values} # {img_path:(folder, feature, feature_path)}
        for f in [1,2]:
            pair_df['img{}_folder'.format(f)] = pair_df['img{}'.format(f)].apply(lambda x:path_folder_dt[x][0])
            pair_df['img{}_feature'.format(f)] = pair_df['img{}'.format(f)].apply(lambda x:path_folder_dt[x][1])      
            pair_df['img{}_feature_path'.format(f)] = pair_df['img{}'.format(f)].apply(lambda x:path_folder_dt[x][2])

        # 是否要計算同個資料夾內的照片
        if not same_folder:
            pair_df = pair_df[pair_df['img1_folder'] != pair_df['img2_folder']]

        print(pair_df.shape[0], "pairs") 
        result["Result"].update({"pair_nums":pair_df.shape[0]})

        sim = []
        for a, b in pair_df[['img1_feature', 'img2_feature']].values:
            sim.append(self.cosine_similarity(a[0], b[0]))

        pair_df['cosine_similarity'] = sim
        result["Result"].update({"similarity_average": pair_df['cosine_similarity'].mean()})
        result["Result"].update({"similarity_variance": pair_df['cosine_similarity'].var()})

        result["Time"].update({"calculate_similarity_timeuse":time.time() - start_time})
        print("time use: ", result["Time"]["calculate_similarity_timeuse"])

        support_nums = pair_df[pair_df.cosine_similarity > sim_threshold].shape[0]
        match_ratio = support_nums / pair_df.shape[0]
        print("\nmatch ratio: ", match_ratio)
        result["Result"].update({"support_nums": support_nums})
        result["Result"].update({"match_ratio":match_ratio})
        result["Result"].update({"match_result":match_ratio>=sup_threshold})

        pair_df.drop(['img1_feature', 'img2_feature'], axis=1, inplace=True)

        result["Time"].update({"Total_timeuse":time.time() - START_time})
        print("\n[Total time use: {}]".format(result["Time"]["Total_timeuse"]))

        if result_table_output:
            pair_df.to_csv(result_table_output, index=False)
        if result_output:
            with open(result_output, "w", encoding='utf8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        return result

    def get_features(self, paths, output_folder, feature_name_level=2, save_feature=False):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        feats = []
        feat_paths = []
        for path in paths:
            assert os.path.exists(path), "Can't find folder at {}".format(path)
            
            name = path.replace('.png','.npy').replace("\\","_").replace("/","_")
            if len(name.split('_')) < feature_name_level:
                feature_name_level = len(name.split('_'))
            name = '_'.join(name.split('_')[-feature_name_level:])

            output_path = os.path.join(output_folder, name)

            if os.path.exists(output_path):
                feat = np.load(output_path)
            else:
                feat = self.image_to_feature(path)
                if save_feature:
                    np.save(output_path, feat)
                    
            feats.append(feat)
            feat_paths.append(output_path)

        return feat_paths, feats

    def match_folders_under_path(self, root_path, output_path, sim_threshold, sup_threshold, sample_nums, sample_in_bin):
        """
        base on `match_two_folder`, compare all of folders under root_path and record result by Dataframe.
        """
        result = []
        file_ls = [os.path.join(root_path, i) for i in os.listdir(root_path) if i.find(".")==-1]
        for f1,f2 in list(itertools.combinations(file_ls, 2)):
            f1_id, f2_id = [i[-1] for i in [f1,f2]]
            output = self.match_two_folder(
                            f1=f1, 
                            f2=f2, 
                            output_folder="{}/{}_{}".format(output_path, f1_id, f2_id), 
                            result_output="{}/{}_{}/result.json".format(output_path, f1_id, f2_id),
                            result_table_output="{}/{}_{}/result.csv".format(output_path, f1_id, f2_id), 
                            sim_threshold=sim_threshold, sup_threshold=sup_threshold, sample_nums=sample_nums,
                            sample_in_bin=sample_in_bin
                            )

            result.append((output['Args']['f1'], output['Args']['f2'],
                        output['Result']['support_nums'], output['Result']['pair_nums'],
                        output['Result']['match_result'], output['Result']['match_ratio'], 
                        output['Time']['Total_timeuse'], output['Result']['similarity_average'],
                        output['Result']['similarity_variance']
                        ))
        
        df = pd.DataFrame(result)
        df.columns = ['f1', 'f2', 'support_nums', 'pair_nums', 'match_result', 'match_ratio', 
                    'Total_timeuse', 'similarity_average', 'similarity_variance']

        match_pair = df.loc[df.match_result, ['f1', 'f2']].values

        if match_pair.shape[0]!=0: 
            result = self._get_group(match_pair.tolist())
            result = [[int(re.search('\d+',f)[0]) for f in gp] for gp in result]
        else:
            result = []

        return df, result
        
    def image_to_feature(self, img_path):
        img = cv2.imread(img_path)
        feat = self.run_on_image(img)
        feat = feat.numpy() 

        return feat  

    def cosine_similarity(self, a, b):
        assert (len(a.shape)==1) & (len(b.shape)==1) & (len(a)==len(b)), "The input vector must be one dimension & same length"
        cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

        return cos_sim

    def _get_random_item(self, input_ls, size, sample_in_bin):
        assert size<=len(input_ls), "The number of samples must be less than the number of images in the folder"

        input_ls = [(int((i.split('.')[0])), i) for i in input_ls]
        input_ls = [i[1] for i in sorted(input_ls)]

        bin_size = len(input_ls)/float(sample_in_bin)
        out = []
        last = 0.0

        while last < len(input_ls):
            out.append(input_ls[int(last):int(last + bin_size)])
            last += bin_size
        # out -> [['12.png', '18.png', '22.png'], ['27.png', '31.png', '48.png'], ...]


        sample_num_in_bin = size // int(bin_size) + 1
        sample_num_in_last_bin = size % sample_num_in_bin

        result = []
        for idx, bin_ls in enumerate(out):
            if (idx+1)!=len(out):
                np.random.shuffle(bin_ls)
                sample = bin_ls[:sample_num_in_bin]
            else:
                np.random.shuffle(bin_ls)
                sample = bin_ls[:sample_num_in_last_bin]
            result.extend(sample)

        return result

    def _warm_up_model(self, path):
        print("\nwarming up model...")
        start_time = time.time()
        _ = self.image_to_feature(path)
        print("time use: ", time.time()-start_time)

    def _check_data(self, root_path):
        if (not os.path.exists(self.config_file)) | (not os.path.exists(self.model_file)):
            print("Can't find pretrain model. start downloading...")
            get_data(root_path)

        for i in [self.config_file, self.model_file]:
            assert os.path.exists(i), "Can't find file at {}".format(i)
            
    def _set_config(self):
        cfg = get_cfg()
        cfg.merge_from_file(self.config_file)
        cfg.MODEL.WEIGHTS = self.model_file
        cfg.freeze()

        return cfg

    def _get_group(self, match_pair_ls):
        groups = [match_pair_ls[0]]
        for pair in match_pair_ls[1:]:
            sign = False
            for idx,_ in enumerate(groups):
                for folder in pair:
                    if folder in groups[idx]:
                        groups[idx].extend(pair)
                        sign = True
                        pass
            if not sign:
                groups.append(pair)
            
        groups = [list(set(gp)) for gp in groups]

        return groups

if __name__ == '__main__':

    demo = ReidMatch(model_file="ReID/pretrain_model",
                     example_img="ReID/predict/img_example.png", # image to warm up model.
                     parallel=False)

    result = demo.match_two_folder('data/1', 'data/2', output_folder="demo/test", 
                                    result_output="demo/test/test.json", result_table_output="demo/test/test.csv", 
                                    sim_threshold=0.8, sup_threshold=0.9, sample_nums=5, sample_in_bin=3)

    df, gp_result = demo.match_folders_under_path(root_path="data", output_path="demo/pairtest",
                                       sim_threshold=0.6, sup_threshold=0.7, sample_nums=5, sample_in_bin=3) 

    df.to_csv("demo/result.csv", index=False)

    # 測試資料
    test = pd.read_csv("data/main.csv")
    for idx,gp in enumerate(result):
        test.loc[test['TID'].isin(gp), 'ReID(predict)'] = idx
    test.fillna(-1, inplace=True)
    test['ReID(predict)'] = test['ReID(predict)'].astype(int)
    test.to_csv("data/main_predict.csv", index=False)

