import sys

input = sys.stdin.read

def main():
    n = int(input().strip())
    
    count = 0
    value = 665
    while count < n:
        value += 1
        if '666' in str(value):
            count += 1
    
    print(value)

if __name__ == "__main__":
    main()
