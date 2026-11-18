import sys

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    cnt = [0] * 26
    for c in s:
        cnt[ord(c) - 97] += 1
    for c in t:
        cnt[ord(c) - 97] -= 1
    print(1 if all(x == 0 for x in cnt) else 0)

main()