"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""
import sys
from FbxReadWriter import FbxReadWrite
from SmplObject import SmplObjects
import argparse
import tqdm
import os
'''
usage:
input_pkl_base: 包含smpl或smplh参数的pkl, 字典组成如下, #!!! 注意该目录下的命名要为  xxx_smpl.pkl或者xxx_smplh.pkl
                {
                    "smpl_poses": (n,66) for smplh or (n,72) for smpl,
                    "smpl_trans": (n,3) 
                }
fbx_source_path: fbx动画文件, 从官方下载的
'''

def getArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pkl_base', type=str, default='./exampl_pkl/')
    parser.add_argument('--output_base', type=str, default='./')

    return parser.parse_args()

if __name__ == "__main__":
    args = getArg()
    input_pkl_base = args.input_pkl_base
    output_base = args.output_base
    standard_models = ['standard_models/SMPL_m_unityDoubleBlends_lbs_10_scale5_207_v1.0.0.fbx',
                       'standard_models/smplh_male_m_avg_noFlatHand.fbx']
    smplObjects = SmplObjects(input_pkl_base)
    for pkl_name, smpl_params in tqdm.tqdm(smplObjects):
        try:
            model_type = pkl_name.split('.')[0]
            if 'smplh' in model_type: 
                fbx_source_path = standard_models[1]
            elif 'smpl' in model_type:
                fbx_source_path = standard_models[0]
            fbxReadWrite = FbxReadWrite(fbx_source_path)
            fbxReadWrite.addAnimation(pkl_name, smpl_params,model_type)
            fbxReadWrite.writeFbx(output_base, pkl_name)
        except Exception as e:
            fbxReadWrite.destroy()
            print ("- - Distroy")
            raise e
        finally:
            fbxReadWrite.destroy()

