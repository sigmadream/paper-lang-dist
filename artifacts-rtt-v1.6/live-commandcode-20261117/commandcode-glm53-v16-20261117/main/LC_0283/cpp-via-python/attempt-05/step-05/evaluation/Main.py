import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    write = 0
    for read in range(n):
        if arr[read] != 0:
            arr[write], arr[read] = arr[read], arr[write]
            write += 1
    print(' '.join(map(str, arr)))

main()