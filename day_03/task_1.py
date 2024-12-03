import re
from icecream import ic

NUM_PATTERN = r"(\d{1,3})"
MUL_REGEXP = re.compile(f"mul\\({NUM_PATTERN},{NUM_PATTERN}\\)")

with open("input.txt") as f:
    content = f.read().strip().replace("\n", "")

# Find all mul() functions
mul_functions = re.findall(MUL_REGEXP, content)

# Extract each (operand_a, operand_b) tuple and multiply them
mul_sum = sum([int(a) * int(b) for (a, b) in mul_functions])

ic(f"Sum when adding the result of all mul() functions: {mul_sum}")
