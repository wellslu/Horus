@echo off 
@REM encoding = "utf8"
@REM for window，設定預測的環境，請先 cd 到本資料夾
conda create -n fastreidPD python=3.7 --yes
conda activate fastreidPD

conda install pytorch==1.6.0 torchvision tensorboard torchaudio cudatoolkit=10.1 -c pytorch --yes

@REM cd [path to root]
pip install -r ReID\predict\requirements
