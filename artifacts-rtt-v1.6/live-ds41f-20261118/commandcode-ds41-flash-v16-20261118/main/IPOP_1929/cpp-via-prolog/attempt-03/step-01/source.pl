sieve([], _, []).
sieve([P|Rest], N, [P|Primes]) :-
    P * P > N,
    !,
    Primes = Rest.
sieve([P|Rest], N, [P|Primes]) :-
    filter_multiples(P, Rest, Rest1),
    sieve(Rest1, N, Primes).

filter_multiples(_, [], []).
filter_multiples(P, [X|Xs], Ys) :-
    (   X mod P =:= 0
    ->  Ys = Ys1
    ;   Ys = [X|Ys1]
    ),
    filter_multiples(P, Xs, Ys1).

print_primes([], _).
print_primes([P|Ps], M) :-
    (   P >= M
    ->  writeln(P)
    ;   true
    ),
    print_primes(Ps, M).

main :-
    read(M),
    read(N),
    findall(X, between(2, N, X), Nums),
    sieve(Nums, N, Primes),
    print_primes(Primes, M).