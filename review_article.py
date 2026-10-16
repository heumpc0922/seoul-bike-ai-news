
# 12단계: AI 기사 자동 검수 기초

import json
import re

# 1. 앞에서 만든 Fact Sheet 읽기
with open("factsheet.json", "r", encoding="utf-16") as f:
    facts = json.load(f)

# 2. 검사할 기사 문장 (연습용)
article = "18시 평균 대여 건수는 약 1,554.02건이었다."

# 3. Fact Sheet에서 실제 평균 확인
peak_hour = facts["peak_hours"][0]
peak_data = facts["hourly"][peak_hour]
correct_mean = peak_data["mean_rentals"]

print("Fact Sheet 기준 평균:", correct_mean, "건")
print("검사할 기사:", article)

# 4. 사람 수로 잘못 표현했는지 검사
if re.search(r"[\d,]+\s*명", article):
    print("경고: 대여 건수를 사람 수로 표현했을 가능성이 있습니다.")
else:
    print("사람 수 표현은 발견되지 않았습니다.")

# 5. 사람이 최종 확인하도록 안내
print("검수 상태: 사람의 최종 확인 필요")

# 13단계: 실제 AI 기사와 Fact Sheet 비교

from pathlib import Path

# 실제 AI 기사 읽기
real_article = Path("article.txt").read_text(encoding="utf-8")

print("\n===== 실제 AI 기사 자동 검수 =====")

# Fact Sheet의 분석 기간 확인
start_date = facts["period_start"]
end_date = facts["period_end"]

# Fact Sheet의 기록 수 확인
raw_rows = facts["raw_rows"]
excluded = facts["excluded_non_operating_rows"]
included = facts["included_rows"]

# 18시 평균과 합계 확인
peak = facts["hourly"][facts["peak_hours"][0]]
peak_total = peak["rental_total"]
peak_count = peak["observations"]
peak_mean = peak["mean_rentals"]

# 검사할 항목
checks = {
    "시작 날짜": start_date in real_article,
    "종료 날짜": end_date in real_article,
    "전체 기록 수": str(raw_rows) in real_article,
    "제외 기록 수": str(excluded) in real_article,
    "분석 기록 수": str(included) in real_article,
    "18시 대여 합계": str(peak_total) in real_article,
    "18시 관측 수": str(peak_count) in real_article,
    "18시 평균": str(peak_mean) in real_article,
}

for name, result in checks.items():
    if result:
        print(f"[확인] {name}: 기준값이 기사에 있음")
    else:
        print(f"[검토] {name}: 기준값을 찾지 못함")

# 사람 수로 표현했는지 확인
if re.search(r"[\d,]+\s*명", real_article):
    print("[경고] 사람 수 표현 발견: 원자료로 확인 필요")
else:
    print("[확인] 숫자 뒤에 '명'이 붙은 표현 없음")

print("\n주의: 이 검사는 값의 등장 여부만 확인합니다.")
print("문장의 의미와 사실 여부는 사람이 최종 검토해야 합니다.")

# 14단계: 시간별 관측 기록의 단위 오류 검사

print("\n===== 단위 오류 자동 검사 =====")

# Fact Sheet에 있는 기록 수
record_numbers = [
    facts["raw_rows"],
    facts["excluded_non_operating_rows"],
    facts["included_rows"]
]

# 기록 수 뒤에 '건'이 붙었는지 검사
for number in record_numbers:
    number_text = f"{number:,}"

    pattern = rf"(?<!\d)(?:{number}|{re.escape(number_text)})\s*건"

    if re.search(pattern, real_article):
        print(f"[경고] {number:,}건: 시간별 관측 기록을 대여 건수처럼 표현했을 가능성")
    else:
        print(f"[확인] {number:,}개의 잘못된 '건' 표현은 발견되지 않음")

print("단위 검사 완료: 사람의 최종 확인 필요")

# 15단계: 기사 자동 검수 보고서 만들기

from datetime import datetime

report_lines = []

report_lines.append("===== AI 기사 자동 검수 보고서 =====")
report_lines.append(f"검사 시각: {datetime.now():%Y-%m-%d %H:%M:%S}")
report_lines.append("자료: UCI Seoul Bike Sharing Demand")
report_lines.append("")

# 숫자·날짜 검사 결과 정리
report_lines.append("[1] 숫자 및 날짜 검사")

for name, result in checks.items():
    if result:
        report_lines.append(f"[확인] {name}: 기준값 발견")
    else:
        report_lines.append(f"[검토 필요] {name}: 기준값 미발견")

# 단위 검사 결과 정리
report_lines.append("")
report_lines.append("[2] 단위 오류 검사")

warning_count = 0

for number in record_numbers:
    number_text = f"{number:,}"
    pattern = rf"(?<!\d)(?:{number}|{re.escape(number_text)})\s*건"

    if re.search(pattern, real_article):
        warning_count += 1
        report_lines.append(
            f"[경고] {number:,}건: 관측 기록을 대여 건수로 표현했을 가능성"
        )

if warning_count == 0:
    report_lines.append("단위 오류 의심 표현을 발견하지 못함")

# 최종 검토 상태
report_lines.append("")
report_lines.append("[3] 최종 검토")
report_lines.append(f"단위 경고 수: {warning_count}")
report_lines.append("자동 검사 결과는 사실 확인 완료를 의미하지 않음")
report_lines.append("최종 상태: 사람의 검토 필요")

# 보고서 파일 저장
report_text = "\n".join(report_lines)

with open("review_report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("\n===== 15단계 완료 =====")
print(report_text)
print("\nreview_report.txt 파일 저장 완료")
