import sys

n = int(sys.stdin.read())
mask = (1 << n) - 1


def search(columns, descending, ascending):
    if columns == mask:
        return 1
    available = mask & ~(columns | descending | ascending)
    count = 0
    while available:
        bit = available & -available
        available -= bit
        count += search(columns | bit, (descending | bit) << 1, (ascending | bit) >> 1)
    return count


# 첫 행을 좌우 반사하여 동등한 두 부분 탐색을 합칩니다.
answer = 0
for column in range(n // 2):
    bit = 1 << column
    answer += 2 * search(bit, bit << 1, bit >> 1)
if n % 2:
    bit = 1 << (n // 2)
    answer += search(bit, bit << 1, bit >> 1)
print(answer)
