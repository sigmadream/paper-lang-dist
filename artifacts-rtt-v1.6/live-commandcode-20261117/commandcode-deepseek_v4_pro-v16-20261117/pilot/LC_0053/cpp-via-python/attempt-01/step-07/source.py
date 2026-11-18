import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    if n == 0:
        return
    nums = list(map(int, data[1:1 + n]))
    cur = nums[0]
    best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    print(best)

if __name__ == "__main__":
    main()