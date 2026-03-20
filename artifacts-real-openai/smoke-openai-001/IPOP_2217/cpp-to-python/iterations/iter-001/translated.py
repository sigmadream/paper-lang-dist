import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    ropes = list(map(int, data[1:1 + n]))
    ropes.sort(reverse=True)

    max_weight = 0
    for i, r in enumerate(ropes):
        current_weight = r * (i + 1)
        if current_weight > max_weight:
            max_weight = current_weight

    sys.stdout.write(str(max_weight) + "\n")

if __name__ == "__main__":
    main()
