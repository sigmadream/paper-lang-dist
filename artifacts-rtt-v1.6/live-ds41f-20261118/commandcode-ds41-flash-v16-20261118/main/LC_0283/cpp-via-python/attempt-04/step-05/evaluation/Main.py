import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    result = [x for x in a if x != 0]
    result.extend([0] * (n - len(result)))

    sys.stdout.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()