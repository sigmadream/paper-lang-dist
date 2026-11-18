import sys

words = sys.stdin.read().split()
for word in words[1:]:
    depth = 0
    for char in word:
        depth += 1 if char == "(" else -1
        if depth < 0:
            break
    print("YES" if depth == 0 else "NO")
