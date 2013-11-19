import primes as p 

if __name__ == '__main__':
    ps = p.primes(101)
    left_to_check = [0] + [1]*100
    for p in ps:
        left_to_check[p] = 0
        n = 1
        while p**n <= 100:
            left_to_check[p**n] = 0
            n += 1
        for q in ps:
            if p*q <= 100:
                left_to_check[p*q] = 0
            else:
                break
            if p*q*q <= 100:
                left_to_check[p*q*q] = 0
            if p*q*q*q <= 100:
                left_to_check[p*q*q*q] = 0
    for i in range(101):
        if left_to_check[i]:
            print i