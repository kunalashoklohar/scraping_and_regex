def mystery(num:int):
    if num == 1:
        return 1
    else:
        return int(f"{num}"*num) + mystery(num-1)


n = 4
print(mystery(n))        