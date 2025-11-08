# 공항 대설 대응 보고 시스템

국내 15개 공항의 대설 대응 상황을 보고하고 본부에서 일괄 조회할 수 있는 시스템입니다.

## 주요 기능

1. **공항별 입력 화면** (`/`)
   - 공항별 대설 대응 상황 보고
   - 정기 보고 시간: 05:10, 11:10, 17:10, 22:10
   - 기상상황, 항공기 운항 현황, 조치사항, 피해 및 복구 입력

2. **공항별 조회 화면** (`/airport/view`)
   - 공항별로 보고한 내용 조회
   - 날짜 및 공항별 필터링

3. **본부 조회 화면** (`/headquarters`)
   - 모든 공항의 보고 내용 일괄 조회
   - 기상상황, 항공기 운항 현황 통계
   - 주요 조치사항 및 피해 복구 현황

## 설치 및 실행

### 1. Python 가상환경 생성 (선택사항)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
python app.py
```

### 4. 브라우저에서 접속
- 공항 입력 화면: http://localhost:5000/
- 공항 조회 화면: http://localhost:5000/airport/view
- 본부 조회 화면: http://localhost:5000/headquarters

## 데이터 저장

모든 보고 데이터는 `data/reports.json` 파일에 저장됩니다.

## 국내 15개 공항

인천, 김포, 김해, 제주, 부산, 대구, 광주, 여수, 울산, 원주, 양양, 청주, 군산, 사천, 포항

## API 엔드포인트

- `POST /api/report` - 보고 제출
- `GET /api/reports` - 보고 조회 (필터링 지원)
- `GET /api/report/<id>` - 특정 보고 조회
- `PUT /api/report/<id>` - 보고 수정
- `DELETE /api/report/<id>` - 보고 삭제
- `GET /api/statistics` - 통계 정보

