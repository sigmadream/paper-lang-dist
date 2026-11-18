import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    s, t = data[0], data[1]
    if len(s) != len(t):
        print(0)
        return
    cnt = [0] * 26
    for c in s:
        cnt[ord(c) - ord('a')] += 1
    for c in t:
        cnt[ord(c) - ord('a')] -= 1
    print(0 if any(x != 0 for x in cnt) else 1)

main()