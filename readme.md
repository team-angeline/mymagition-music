# API-Automatic-Music

Team Angline에서 사용하는 자체 자동화 API Server로 음악 및 화성학 관련된 자동화 알고리즘을 주로 
배포합니다.

## 현재 배포중인 기능들
| Name                                          | Summary                              |
|-----------------------------------------------|--------------------------------------|
| [RCFL](https://github.com/team-angeline/pcfl) | FL Studio에서의 CC64 Import를 위한 교정 알고리즘 |

## How to install
1. Install Python (3.10 이상)
2. 가상머신 생성 및 Package 설치 ```pip install -r requirements.txt```
3. .env 파일 생성
```bash
SERVER_PORT="int"
SERVER_MODE="dev or prod"
# dev -> 개발모드
# prod -> 배포모드
```
4. ```$ python main.py``` 로 서버 실행
