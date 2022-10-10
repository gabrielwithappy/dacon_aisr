This is the code for Dacon aisr
박수철, 장진우, 윤성국, 양성모

o   코드에 ‘/data’ 데이터 입/출력 경로 포함


o   모든 코드는 오류 없이 실행되어야 함(라이브러리 로딩 코드 포함)

o   개발 환경(OS) 및 라이브러리 버전 기재

o   외부 데이터 사용 시 출처와 다운로드 링크

o   사전 학습 모델 사용 시 출처와 (별도 필요시) 다운로드 링크

솔루션 설명 PPT 자료

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