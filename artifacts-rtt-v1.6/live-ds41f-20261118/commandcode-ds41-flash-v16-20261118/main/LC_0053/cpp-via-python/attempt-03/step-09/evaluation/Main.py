import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n <= 0 or len(data) < 2:
        return
    x = int(data[1])
    cur = x
    best = x
    for i in range(2, n + 1):
        x = int(data[i])
        cur = x if x > cur + x else cur + x
        if cur > best:
            best = cur
    sys.stdout.write(str(best) + "\n")

main()