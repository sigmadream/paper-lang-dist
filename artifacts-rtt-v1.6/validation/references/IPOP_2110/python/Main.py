import sys

n, count, *houses = map(int, sys.stdin.buffer.read().split())
houses.sort()
lo, hi, answer = 1, houses[-1] - houses[0], 0
while lo <= hi:
    gap = (lo + hi) // 2
    placed, previous = 1, houses[0]
    for house in houses[1:]:
        if house - previous >= gap:
            placed += 1
            previous = house
    if placed >= count:
        answer, lo = gap, gap + 1
    else:
        hi = gap - 1
print(answer)
