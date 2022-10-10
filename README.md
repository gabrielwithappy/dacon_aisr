This is the code for Dacon aisr
박수철, 장진우, 윤성국, 양성모

OS : ubuntu
Python : > 3.7
Links:
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
-- test files should be copied to /Real-ESRGAN/inputs
-- trained model should be copied to /Real-ESRGAN/tags
-- ensemble result goes to /utility/ensemble/result
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