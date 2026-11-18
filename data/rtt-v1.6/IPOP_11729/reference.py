import sys

n = int(sys.stdin.read())
moves = []


def hanoi(size, source, auxiliary, target):
    if size == 0:
        return
    hanoi(size - 1, source, target, auxiliary)
    moves.append(f"{source} {target}")
    hanoi(size - 1, auxiliary, source, target)


hanoi(n, 1, 2, 3)
print(len(moves))
sys.stdout.write("\n".join(moves) + "\n")
