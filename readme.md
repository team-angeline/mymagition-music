# mymagition-music

<div align="center">
    <img src="https://img.shields.io/badge/Python 3.10-FFD43B?style=flat-square&logo=python&logoColor=blue" />
    <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=flat-square&logo=docker&logoColor=white" />
</div>


잡동사니 알고리즘 API Service Mymagition에 사용되는 Microservice API

## 제공중인 서비스
### PCFL

[Repo](https://github.com/team-angeline/pcfl)

#### Introduce
FL Studio에서 Midi 파일의 연속된 피아노 페달을 붙임 없이 임포트 하기 위해 페달 사이의 간격을 벌리는 전처리 작업을 하는 기능
#### API Parameter
* URL: {host}/pcfl
* Method: POST

* 파일을 입력으로 받기 때문에 JSON이 아닌 Form 형태로 요청해야 합니다.
```json
{
    "file": "<File Data (Midi)>",
    "interval": "<0.1 이상 0.6 미만의 실수값>"
}
```


## How to install
1. Python 3.10.6 이상
2. Python 가상머신 생성
3. Submodule과 함께 가져오기 ```git clone [repository] --recursive```
4. ```pip install --upgrade pip```
5. ```pip install -r requirements.txt```
6. 아래와 같이 ```.env``` 파일을 작성합니다.
    ```bash
    SERVER_PORT="int"
    SERVER_MODE="<개발용일 경우 dev, 배포용일 경우 prod>"
    ```
7. <개발용>일 경우 ```python app.py```
8. <배포 테스트>일 경우 ```sh bin/run.sh```