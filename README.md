AI 양재 허브 인공지능 오픈소스 경진대회 1위

이미지 초해상화(Image Super-Resolution)를 위한 AI 알고리즘 개발
품질이 저하된 저해상도 촬영 이미지(512X512)를 고품질의 고해상도 촬영 이미지(2048X2048)로 생성
주최: AI 양재 허브
주관: 데이콘
https://dacon.io/competitions/official/235977/codeshare/6887

# Team Members
박수철, 장진우, 윤성국, 양성모

# Environment
- OS : ubuntu
- Python : > 3.7
- Links:
  - [Real ESRGAN](https://github.com/xinntao/Real-ESRGAN)


# Configuration
1. create collab notebook on your google drive root.
2. connect your google drive by using below code on the your collab notebook
   then all code will be in the dacon_aisr folder
```
from google.colab import drive
drive.mount('/content/drive')

%cd '/content/drive/MyDrive/'
!git clone https://github.com/gabrielwithappy/dacon_aisr.git

```

# Code detail
```
- Real-ESGAN
  L archs
      L rrdbnet_selfensemble_arch.py : use self-ensemble of the model (Rotation, Flip)
      L ***.py : model pipeline (body - upsample - body -upsample -outlayer)
- Real-ESGAN-interence.ipynb : soft ensemble of models
- options/****.yml : train hyper parameter
```

# Inference
- user/dacon_aisr/Real-ESGAN_inference notebook
- follow configuration step of the notebook
- test files should be copied to /Real-ESRGAN/inputs
- trained model should be copied to /Real-ESRGAN/tags
- ensemble result goes to /utility/ensemble/result


:Folder Structure:
```
/Real-ESRGAN
  ㄴ inputs
/tags
/utility
  ㄴ ensemble
    ㄴ model_1
    ㄴ model_2
    ㄴ model_3
    ㄴ model_4
    ㄴ result (the ensemble images of models )
```
