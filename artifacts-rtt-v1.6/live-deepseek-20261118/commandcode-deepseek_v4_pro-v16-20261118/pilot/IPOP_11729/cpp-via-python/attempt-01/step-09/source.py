import sys

def hanoi(n, fr, via, to, out):
    if n == 1:
        out.append(f"{fr} {to}\n")
        return
    hanoi(n - 1, fr, to, via, out)
    out.append(f"{fr} {to}\n")
    hanoi(n - 1, via, fr, to, out)

def main():
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())

    out = [f"{(1 << n) - 1}\n"]
    hanoi(n, 1, 2, 3, out)
    sys.stdout.write(''.join(out))

if __name__ == "__main__":
    main()