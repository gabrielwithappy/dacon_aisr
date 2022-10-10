This is the code for Dacon aisr
박수철, 장진우, 윤성국, 양성모

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
      l rrdbnet_selfensemble_arch.py : use self-ensemble of the model (Rotation, Flip)
      l ***.py : model pipeline (body - upsample - body -upsample -outlayer)
- Real-ESGAN-interence.ipynb : soft ensemble of models
- options/****.yml : train hyper parameter
```