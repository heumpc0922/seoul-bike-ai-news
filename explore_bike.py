
import csv

with open('data/SeoulBikeData.csv', encoding='latin1', newline='') as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    rows = list(reader)

print("전체 데이터 행 수:", len(rows))
print("전체 데이터 열 수:", len(columns))

print("첫 번째 데이터:", rows[0]['Date'], rows[0]['Hour'], rows[0]['Rented Bike Count'])

# 4단계: 운영 시간만 골라 평균 계산하기

operating = [row for row in rows if row['Functioning Day'] == 'Yes']

total = sum(int(row['Rented Bike Count']) for row in operating)

print("전체 행:", len(rows))
print("운영 행:", len(operating))
print("제외 행:", len(rows) - len(operating))
print("대여 합계:", total)
print("전체 시간 평균:", round(total / len(rows), 1))
print("운영 시간 평균:", round(total / len(operating), 1))

# 5단계: 오후 6시(18시) 평균 대여 건수 계산하기

hour18 = [row for row in operating if int(row['Hour']) == 18]

total18 = sum(int(row['Rented Bike Count']) for row in hour18)

print("18시 대여 합계:", total18)
print("18시 관측 수:", len(hour18))
print("18시 평균:", round(total18 / len(hour18), 2))

# 6단계: 0시부터 23시까지 평균 대여 건수 계산

hourly_averages = {}

for hour in range(24):
    hour_rows = [
        row for row in operating
        if int(row['Hour']) == hour
    ]

    total_hour = sum(
        int(row['Rented Bike Count'])
        for row in hour_rows
    )

    count_hour = len(hour_rows)

    average = total_hour / count_hour if count_hour > 0 else 0

    hourly_averages[hour] = average

    print(f"{hour:02d}시: {average:.2f}건")

# 평균이 가장 높은 시간대 찾기
peak_hour = max(hourly_averages, key=hourly_averages.get)

print("--------------------------")
print(f"평균 대여가 가장 많은 시간: {peak_hour}시")
print(f"해당 시간 평균: {hourly_averages[peak_hour]:.2f}건")
