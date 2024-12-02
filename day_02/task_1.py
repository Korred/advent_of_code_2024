from icecream import ic

with open("input.txt", "r") as file:
    reports = [list(map(int, line.split())) for line in file]


safe_reports = 0

for report in reports:
    # Ensures the report is strictly increasing or decreasing
    if report == sorted(report) or report == sorted(report, reverse=True):
        diffs = [abs(b - a) for a, b in zip(report, report[1:])]

        # Ensures the differences between the numbers are between 1 and 3
        if all(1 <= diff <= 3 for diff in diffs):
            safe_reports += 1

ic(f"The number of safe reports is: {safe_reports}")
