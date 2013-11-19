from array import *

def sieve(N):
    sieve = [1]*N
    sieve[0] = 0
    sieve[1] = 0
    primes = [2]
    for i in xrange(4,N,2):
        sieve[i] = 0
    for i in xrange(3, int(N ** 0.5) + 1,2):
        if sieve[i]:
            primes.append(i)
            for j in xrange(i << 1, N, i):
                sieve[j] = 0
    return sieve

def primes(N):
    sieve = [1]*N
    sieve[0] = 0
    sieve[1] = 0 
    primes = [2]
    for i in xrange(4,N,2):
        sieve[i] = 0
    for i in xrange(3, int(N ** 0.5) + 1,2):
        if sieve[i]:
            primes.append(i)
            for j in xrange(i << 1, N, i):
                sieve[j] = 0
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # return sieve
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    start = int((int(N)**.5)+1)
    if not start % 2:
        start += 1
    for i in xrange(start,N,2):
        if sieve[i]:
            primes.append(i)
    return primes

def p_factors(N):
    sieve = [1]*N
    sieve[0] = 0
    sieve[1] = 0 
    primes = [2]
    for i in xrange(4,N,2):
        sieve[i] = 0
    for i in xrange(3, int(N ** 0.5) + 1,2):
        if sieve[i]:
            primes.append(i)
            for j in xrange(i << 1, N, i):
                sieve[j] = 0
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # return sieve
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    start = int((int(N)**.5)+1)
    if not start % 2:
        start += 1
    for i in xrange(start,N,2):
        if sieve[i]:
            primes.append(i)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # return primes
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    p_length = len(primes)
    p_factors = {}
    for n in xrange(2,N):
        if sieve[n]:
            p_factors[n] = [n]
            continue
        for i in xrange(0,p_length):
            if n % primes[i] == 0:
                p_factors[n] = sorted([primes[i]]+p_factors[n/primes[i]])
                break
    return p_factors

def p_factors_cond(N):
    sieve = [1]*N
    sieve[0] = 0
    sieve[1] = 0 
    primes = [2]
    for i in xrange(4,N,2):
        sieve[i] = 0
    for i in xrange(3, int(N ** 0.5) + 1,2):
        if sieve[i]:
            primes.append(i)
            for j in xrange(i << 1, N, i):
                sieve[j] = 0
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # return sieve
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    start = int((int(N)**.5)+1)
    if not start % 2:
        start += 1
    for i in xrange(start,N,2):
        if sieve[i]:
            primes.append(i)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # return primes
    # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    p_length = len(primes)
    p_factors = {}
    for n in xrange(2,N):
        if sieve[n]:
            p_factors[n] = [n]
            continue
        for i in xrange(0,p_length):
            if n % primes[i] == 0:
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                # if you don't want it condensed, comment out next three lines
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                if primes[i] in p_factors[n/primes[i]]:
                    p_factors[n] = p_factors[n/primes[i]]
                    break
                p_factors[n] = sorted([primes[i]]+p_factors[n/primes[i]])
                break
    return p_factors
