def karatsuba(x, y):
    x = str(x)
    y = str(y)
    if len(x) == 1 or len(y) == 1:
        return int(x) * int(y)

    x_digits = len(x)
    y_digits = len(y)
    x_head, x_end = x[:x_digits // 2], x[x_digits // 2:]
    y_head, y_end = y[:y_digits // 2], y[y_digits // 2:]

    ac = karatsuba(int(x_head), int(y_head)) * (10 ** (len(x_end) + len(y_end)))
    db = karatsuba(int(x_end), int(y_end))
    ad = karatsuba(int(x_head), int(y_end)) * (10 ** len(x_end))
    dc = karatsuba(int(y_head), int(x_end)) * (10 ** len(y_end))
    result = ac + db + ad + dc
    return result

if __name__ == '__main__':
    print(karatsuba(3141592653589793238462643383279502884197169399375105820974944592,
                    2718281828459045235360287471352662497757247093699959574966967627))
    print(3141592653589793238462643383279502884197169399375105820974944592 * 2718281828459045235360287471352662497757247093699959574966967627)
    #
    # print(karatsuba(578, 1234))