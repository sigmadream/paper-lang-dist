import sys
from math import isqrt

low, high = map(int, sys.stdin.buffer.read().split())
prime = bytearray(b"\x01") * (high + 1)
prime[:2] = b"\x00\x00"
for divisor in range(2, isqrt(high) + 1):
    if prime[divisor]:
        prime[divisor * divisor : high + 1 : divisor] = b"\x00" * (
            (high - divisor * divisor) // divisor + 1
        )
sys.stdout.write(
    "\n".join(str(number) for number in range(low, high + 1) if prime[number]) + "\n"
)
