import re
from icecream import ic

NUM_PATTERN = r"(\d{1,3})"
MUL_PATTERN = f"(mul)\\({NUM_PATTERN},{NUM_PATTERN}\\)"
DO_PATTERN = r"(do)\(\)"
DONT_PATTERN = r"(don't)\(\)"

FUNCTIONS_REGEXP = re.compile(f"{MUL_PATTERN}|{DO_PATTERN}|{DONT_PATTERN}")

with open("input.txt") as f:
    content = f.read().strip().replace("\n", "")


functions = FUNCTIONS_REGEXP.findall(content)

last_modifier = "do"
mul_sum = 0

for mul, a, b, do, dont in functions:
    if mul and last_modifier == "do":
        mul_sum += int(a) * int(b)
    else:
        last_modifier = do or dont

ic(f"Sum when adding the result of all enabled mul() functions: {mul_sum}")
