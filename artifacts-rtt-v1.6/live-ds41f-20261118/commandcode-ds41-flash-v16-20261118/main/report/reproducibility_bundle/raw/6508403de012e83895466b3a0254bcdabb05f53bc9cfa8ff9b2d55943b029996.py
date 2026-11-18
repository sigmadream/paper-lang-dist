import sys
from collections import Counter

left, right = sys.stdin.read().split()
print(int(Counter(left) == Counter(right)))
