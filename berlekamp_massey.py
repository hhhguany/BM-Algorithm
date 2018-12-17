# -*- coding: UTF-8 -*-
__all__ = ["simple_bm", "print_int_polynome", "int_to_bin"]

flow1 = [0, 1, 0, 1, 0, 1, 0]
flow2 = [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0]


def simple_bm(flow, **arg):
    n, l, fx = 0, [], []

    # 初始化
    '''
    flow = [0, 1, 0, 1, 0, 1, 0]
    n=2 -> a(n-1)=a(1)=1
    '''
    for i in flow:
        if i == 1: break
        n += 1
    '''
    >> i=0 i=1 >>
    l(0)=l(1)=0
    fx(0)=fx(1)=1
    '''
    for i in range(n + 1):
        l.append(0)
        fx.append(1)
    l.append(n + 1)
    m = n
    fx.append(bin_to_int(xor(int_to_bin(fx[-1]), exponent_to_bin(n + 1))))

    if "debug" in arg:
        print_int_polynome(int_to_bin(fx[-1]), with_fx=n + 1)
        print()

    n += 1

    while n < len(flow):
        d = bin_sum(xor(flow[:n + 1], int_to_bin(fx[-1])[::-1], 'right&'))
        if d == 0:
            fx.append(fx[-1])
            l.append(l[-1])
        else:
            '''
            f(n+1)(x) = fn(x)+dn dm^-1 x^(n-m) fm(x)
            '''
            fx.append(bin_to_int(xor(int_to_bin(fx[-1]), polynome_multiply(exponent_to_bin(n - m), int_to_bin(fx[m])))))

            if l[-1] >= n + 1 - l[-1]:
                l.append(l[-1])
            else:
                l.append(n + 1 - l[-1])
                m = n
            if "debug" in arg:
                print_int_polynome(int_to_bin(fx[-1]), with_fx=n + 1)
                print()
        n += 1
    return [fx[-1], l[-1]]


def bin_sum(_bin):
    '''
    bin_sum([1,1]) = 0
    bin_sum([1,1,1]) = 1
    '''
    out = 0
    for i in _bin:
        out = out ^ i
    return out


def int_to_bin(_int):
    '''
    int_to_bin(15) = [1, 1, 1, 1]
    '''
    return [int(i) for i in list(bin(_int)[2:])]


def int_xor(_int1, _int2):
    return xor(int_to_bin(_int1), int_to_bin(_int2))


def bin_to_int(_bin):
    '''
    bin_to_int(['1', '1', '1', '1']) = 15
    '''
    out = ""
    for i in _bin:
        out += str(i)
    return int(out, 2)


def xor(_bin1, _bin2, mode='left'):
    '''
    xor([1, 0, 0, 0, 1, 0], [1, 0, 1, 1, 0],"right")=[1, 1, 0, 1, 0, 0]
    '''
    if len(_bin1) < len(_bin2):
        _bin1, _bin2 = _bin2, _bin1
    if mode == 'left':
        return [_bin1[i] ^ _bin2[i] for i in range(len(_bin2))] + _bin1[len(_bin2):]
    elif mode == 'right':
        return _bin1[:len(_bin1) - len(_bin2)] + [_bin1[len(_bin1) - len(_bin2) + i] ^ _bin2[i] for i in range(len(_bin2))]
    elif mode == "right&":
        return [0 for i in range(len(_bin1) - len(_bin2))] + [_bin1[len(_bin1) - len(_bin2) + i] & _bin2[i] for i in range(len(_bin2))]
    elif mode == "left&":
        return [_bin1[i] & _bin2[i] for i in range(len(_bin2))] + [0 for i in range(len(_bin1) - len(_bin2))]
    else:
        raise AttributeError
    # for j in range(len(_bin2))


def exponent_to_bin(exponent):
    '''
    x^2 => [0,0,1]
    exponent_to_bin(2) = [0,0,1]
    '''
    return [0 for i in range(exponent)] + [1]


def polynome_multiply(polynome1, polynome2):
    '''
    (x + x^2) * (x^2 + x^3 + x^6) = x^3 + x^5 + x^7 + x^8
    polynome_multiply([0,1,1],[0,0,1,1,0,0,1,0])=[0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
    '''
    out = []
    for i in range(len(polynome1)):
        if polynome1[i] == 1:
            out = xor(out, [0 for j in range(i)] + polynome2)
    return out


def print_int_polynome(_bin, **arg):
    '''
    f(255) = 1 + x + x^2 + x^3 + x^4 + x^5 + x^6 + x^7
    '''
    start = False
    if "with_fx" in arg and arg["with_fx"] == 0:
        print("f(x) =", end="")
    elif "with_fx" in arg and arg["with_fx"] != 0:
        print("f" + str(arg["with_fx"]) + "(x) =", end="")
    if _bin[0] == 1:
        print(" 1", end="")
        start = True
    if _bin[1] == 1:
        if start: print(" + x", end="")
        else:
            print(" x", end="")
            start = True
    for i in range(len(_bin) - 2):
        if _bin[i + 2] == 1:
            if start: print(" + x^" + str(i + 2), end="")
            else:
                print(" x^" + str(i + 2), end="")
                start = True


def test_polynome_multiply():
    a = [0, 0, 1, 1, 0, 0, 1, 0]
    print_int_polynome(a)
    b = polynome_multiply([0, 1, 1], a)
    print(b)
    print(exponent_to_bin(2))


def test_xor():
    a = int_to_bin(34)
    b = int_to_bin(22)
    c = xor(a, b, "right")
    print(a)
    print(b)
    print(c)


def test_bm():
    [fx, l] = simple_bm(flow2, debug=True)
    print_int_polynome(int_to_bin(fx), with_fx=0)


if __name__ == "__main__":
    test_bm()