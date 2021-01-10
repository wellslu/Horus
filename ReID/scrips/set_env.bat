@echo off 
@REM for window，設定train 的環境
conda create -n fastreid python=3.7
conda activate fastreid

conda install faiss-cpu -c pytorch
conda install pytorch==1.6.0 torchvision tensorboard torchaudio cudatoolkit=10.1 -c pytorch --yes

cd ..\train
pip install -r requirements

cd fastreid\evaluation\rank_cylib
!make all