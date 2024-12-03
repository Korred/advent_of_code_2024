import re
from icecream import ic

NUM_PATTERN = r"(\d{1,3})"
MUL_REGEXP = re.compile(f"(mul)\\({NUM_PATTERN},{NUM_PATTERN}\\)")
DO_REGEXP = re.compile(r"(do)\(\)")
DONT_REGEXP = re.compile(r"(don't)\(\)")

with open("input.txt") as f:
    content = f.read().strip().replace("\n", "")

mul_functions = [
    # (index, "mul", operand_a, operand_b)
    (match.start(0), "mul", match.group(2), match.group(3))
    for match in re.finditer(MUL_REGEXP, content)
]
do_functions = [(match.start(0), "do") for match in re.finditer(DO_REGEXP, content)]
dont_functions = [
    (match.start(0), "don't") for match in re.finditer(DONT_REGEXP, content)
]

# Join mul, do and dont functions into one list and sort them by index
functions = sorted(mul_functions + do_functions + dont_functions, key=lambda x: x[0])

last_modifier = "do"
mul_sum = 0

for func in functions:
    func_type = func[1]

    # Only run the mul() function if the last modifier was "do"
    if func_type == "mul" and last_modifier == "do":
        mul_sum += int(func[2]) * int(func[3])
    else:
        last_modifier = func_type

ic(f"Sum when adding the result of all enabled mul() functions: {mul_sum}")
