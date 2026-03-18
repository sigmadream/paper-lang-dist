import sys

def main():
    data = sys.stdin.readline().strip()
    n = int(data)

    count = 0
    value = 665
    while count < n:
        value += 1
        if "666" in str(value):
            count += 1

    sys.stdout.write(str(value) + "\n")

if __name__ == "__main__":
    main()
