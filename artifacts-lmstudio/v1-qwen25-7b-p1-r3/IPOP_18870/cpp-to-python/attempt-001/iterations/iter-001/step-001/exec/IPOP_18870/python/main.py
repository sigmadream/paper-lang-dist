import sys
from typing import List

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    sorted_a = sorted(set(a))
    compressed = {x: i for i, x in enumerate(sorted_a)}
    
    for x in a:
        print(compressed[x], end=" ")
    print()

if __name__ == "__main__":
    main()
