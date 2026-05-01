n = int(input())

count = 0
value = 665
while count < n:
    value += 1
    str_value = str(value)
    if "666" in str_value:
        count += 1

print(value)
