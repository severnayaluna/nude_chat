from functools import lru_cache


@lru_cache
def f(a, b):
    if a + b > 50:
        return 0
    ap = [f(a + 2, b), f(a * 2, b), f(a, b + 2), f(a, b * 2)]
    lte_0 = [i for i in ap if i <= 0]

    if lte_0:
        return -max(lte_0)+1
    else:
        return -max(ap)

for i in range(1, 10):
    print(i, f(i, 2))