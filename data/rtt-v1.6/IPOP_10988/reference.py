import sys

word = sys.stdin.read().strip()
print(int(word == word[::-1]))
