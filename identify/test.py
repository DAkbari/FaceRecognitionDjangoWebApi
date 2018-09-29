def myFunc(n):
    return lambda a: a*n

cusFunct = myFunc(2)
print(cusFunct(11))