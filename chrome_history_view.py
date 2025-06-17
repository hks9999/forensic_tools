
import sqlite3
import os
import shutil
from pathlib import Path
import datetime
import csv

# 사용자 홈 디렉토리
home = str(Path.home())

# Chrome 다운로드 기록 위치
history_path = os.path.join(
    home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
)

history_path ='history'

# 파일 복사 (열려 있을 수 있으므로 복사본 사용)
tmp_history = 'history_copy'
shutil.copy2(history_path, tmp_history)

# SQLite 연결
conn = sqlite3.connect(tmp_history)
cursor = conn.cursor()

# 다운로드 기록 추출 (최신 10개)
cursor.execute("""
    SELECT target_path, tab_url, start_time, end_time, total_bytes, referrer
    FROM downloads
    ORDER BY start_time
""")

# Webkit timestamp → datetime 변환 함수
def from_webkit_time(wt):
    if wt:
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=wt)
    return None

# CSV 파일로 출력
csv_file = 'chrome_download_history.csv'

# CSV 파일 헤더 작성
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Start Time', 'Downloaded File', 'URL'])  # 헤더 작성
    
    # 결과 출력 및 CSV에 기록
    for row in cursor.fetchall():
        start_time = from_webkit_time(row[2])  # start_time 변환
        downloaded_file = row[0]
        url = row[1]
        
        # 데이터 기록
        writer.writerow([start_time, downloaded_file, url])

# 종료
conn.close()
os.remove(tmp_history)

print(f"CSV 파일 '{csv_file}'로 다운로드 기록을 저장했습니다.")
