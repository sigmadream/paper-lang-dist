import sys

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    cnt = [0] * 26
    for c in s:
        cnt[ord(c) - ord('a')] += 1
    for c in t:
        cnt[ord(c) - ord('a')] -= 1
    print(1 if all(v == 0 for v in cnt) else 0)

main()