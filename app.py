from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'airport-snow-response-system'

# 데이터 저장 디렉토리
DATA_DIR = 'data'
REPORTS_FILE = os.path.join(DATA_DIR, 'reports.json')

# 국내 15개 공항 목록
AIRPORTS = [
    '인천', '김포', '김해', '제주', '부산', '대구', '광주', 
    '여수', '울산', '원주', '양양', '청주', '군산', '사천', '포항'
]

# 정기 보고 시간
REPORT_TIMES = ['05:10', '11:10', '17:10', '22:10']

# 데이터 디렉토리 생성
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 데이터 파일 초기화
if not os.path.exists(REPORTS_FILE):
    with open(REPORTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_reports():
    """보고 데이터 로드"""
    try:
        with open(REPORTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_reports(reports):
    """보고 데이터 저장"""
    with open(REPORTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)

def get_next_id():
    """다음 ID 생성"""
    reports = load_reports()
    if not reports:
        return 1
    return max([r.get('id', 0) for r in reports]) + 1

# 공항 입력 화면
@app.route('/')
def airport_input():
    """공항 입력 화면"""
    return render_template('airport_input.html', airports=AIRPORTS, report_times=REPORT_TIMES)

# 공항별 조회 화면
@app.route('/airport/view')
def airport_view():
    """공항별 조회 화면"""
    return render_template('airport_view.html', airports=AIRPORTS)

# 본부 조회 화면
@app.route('/headquarters')
def headquarters():
    """본부 조회 화면"""
    return render_template('headquarters.html', airports=AIRPORTS, report_times=REPORT_TIMES)

# 보고 제출 API
@app.route('/api/report', methods=['POST'])
def submit_report():
    """공항 보고 제출"""
    try:
        data = request.get_json()
        
        # 필수 필드 검증
        if not data.get('airport') or not data.get('report_time') or not data.get('report_date'):
            return jsonify({'success': False, 'message': '공항, 보고시간, 보고일자는 필수입니다.'}), 400
        
        # 새 보고 생성
        report = {
            'id': get_next_id(),
            'airport': data.get('airport'),
            'report_date': data.get('report_date'),
            'report_time': data.get('report_time'),
            'weather': {
                'snowfall_area': data.get('weather', {}).get('snowfall_area', ''),
                'snowfall_amount': data.get('weather', {}).get('snowfall_amount', ''),
                'cumulative_snowfall': data.get('weather', {}).get('cumulative_snowfall', ''),
                'preliminary_warning': data.get('weather', {}).get('preliminary_warning', False),
                'advisory': data.get('weather', {}).get('advisory', False),
                'warning': data.get('weather', {}).get('warning', False),
                'special_notes': data.get('weather', {}).get('special_notes', '')
            },
            'flight_status': {
                'international': {
                    'planned_total': int(data.get('flight_status', {}).get('international', {}).get('planned_total', 0) or 0),
                    'planned_today': int(data.get('flight_status', {}).get('international', {}).get('planned_today', 0) or 0),
                    'pre_cancelled': int(data.get('flight_status', {}).get('international', {}).get('pre_cancelled', 0) or 0),
                    'cancelled_total': int(data.get('flight_status', {}).get('international', {}).get('cancelled_total', 0) or 0),
                    'cancelled_today': int(data.get('flight_status', {}).get('international', {}).get('cancelled_today', 0) or 0),
                    'cancelled_pre': int(data.get('flight_status', {}).get('international', {}).get('cancelled_pre', 0) or 0)
                },
                'domestic': {
                    'planned_total': int(data.get('flight_status', {}).get('domestic', {}).get('planned_total', 0) or 0),
                    'planned_today': int(data.get('flight_status', {}).get('domestic', {}).get('planned_today', 0) or 0),
                    'pre_cancelled': int(data.get('flight_status', {}).get('domestic', {}).get('pre_cancelled', 0) or 0),
                    'cancelled_total': int(data.get('flight_status', {}).get('domestic', {}).get('cancelled_total', 0) or 0),
                    'cancelled_today': int(data.get('flight_status', {}).get('domestic', {}).get('cancelled_today', 0) or 0),
                    'cancelled_pre': int(data.get('flight_status', {}).get('domestic', {}).get('cancelled_pre', 0) or 0)
                }
            },
            'actions': {
                'snow_removal': data.get('actions', {}).get('snow_removal', ''),
                'deicing': data.get('actions', {}).get('deicing', ''),
                'other': data.get('actions', {}).get('other', '')
            },
            'damage_recovery': data.get('damage_recovery', ''),
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 데이터 저장
        reports = load_reports()
        reports.append(report)
        save_reports(reports)
        
        return jsonify({'success': True, 'message': '보고가 성공적으로 제출되었습니다!', 'id': report['id']})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

# 공항별 보고 조회 API
@app.route('/api/reports', methods=['GET'])
def get_reports():
    """보고 조회 (필터링 지원)"""
    try:
        airport = request.args.get('airport')
        report_date = request.args.get('report_date')
        report_time = request.args.get('report_time')
        
        reports = load_reports()
        
        # 필터링
        if airport:
            reports = [r for r in reports if r.get('airport') == airport]
        if report_date:
            reports = [r for r in reports if r.get('report_date') == report_date]
        if report_time:
            reports = [r for r in reports if r.get('report_time') == report_time]
        
        # 최신순 정렬
        reports.sort(key=lambda x: (x.get('report_date', ''), x.get('report_time', '')), reverse=True)
        
        return jsonify({'success': True, 'data': reports})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

# 특정 보고 조회 API
@app.route('/api/report/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """특정 보고 조회"""
    try:
        reports = load_reports()
        report = next((r for r in reports if r.get('id') == report_id), None)
        
        if not report:
            return jsonify({'success': False, 'message': '보고를 찾을 수 없습니다.'}), 404
        
        return jsonify({'success': True, 'data': report})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

# 보고 수정 API
@app.route('/api/report/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    """보고 수정"""
    try:
        data = request.get_json()
        reports = load_reports()
        
        report = next((r for r in reports if r.get('id') == report_id), None)
        if not report:
            return jsonify({'success': False, 'message': '보고를 찾을 수 없습니다.'}), 404
        
        # 데이터 업데이트
        report.update({
            'airport': data.get('airport', report.get('airport')),
            'report_date': data.get('report_date', report.get('report_date')),
            'report_time': data.get('report_time', report.get('report_time')),
            'weather': data.get('weather', report.get('weather')),
            'flight_status': data.get('flight_status', report.get('flight_status')),
            'actions': data.get('actions', report.get('actions')),
            'damage_recovery': data.get('damage_recovery', report.get('damage_recovery')),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        save_reports(reports)
        return jsonify({'success': True, 'message': '보고가 수정되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

# 보고 삭제 API
@app.route('/api/report/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """보고 삭제"""
    try:
        reports = load_reports()
        reports = [r for r in reports if r.get('id') != report_id]
        save_reports(reports)
        return jsonify({'success': True, 'message': '보고가 삭제되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

# 통계 API (본부 조회용)
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """통계 정보 조회"""
    try:
        report_date = request.args.get('report_date')
        report_time = request.args.get('report_time')
        
        reports = load_reports()
        
        if report_date:
            reports = [r for r in reports if r.get('report_date') == report_date]
        if report_time:
            reports = [r for r in reports if r.get('report_time') == report_time]
        
        # 통계 계산
        stats = {
            'total_reports': len(reports),
            'airports_with_snow': [],
            'airports_with_warnings': [],
            'total_cancellations': {
                'international': 0,
                'domestic': 0,
                'total': 0
            }
        }
        
        for report in reports:
            weather = report.get('weather', {})
            if weather.get('snowfall_amount') or weather.get('cumulative_snowfall'):
                if report.get('airport') not in stats['airports_with_snow']:
                    stats['airports_with_snow'].append(report.get('airport'))
            
            if weather.get('preliminary_warning') or weather.get('advisory') or weather.get('warning'):
                if report.get('airport') not in stats['airports_with_warnings']:
                    stats['airports_with_warnings'].append(report.get('airport'))
            
            flight = report.get('flight_status', {})
            stats['total_cancellations']['international'] += flight.get('international', {}).get('cancelled_total', 0)
            stats['total_cancellations']['domestic'] += flight.get('domestic', {}).get('cancelled_total', 0)
        
        stats['total_cancellations']['total'] = stats['total_cancellations']['international'] + stats['total_cancellations']['domestic']
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
