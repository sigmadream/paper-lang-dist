:- use_module(library(lists)).

main :-
    read_input(M, N),
    Limit is floor(sqrt(N)),
    primes_upto(Limit, SmallPrimes),
    numlist(M, N, Nums),
    sieve_interval(Nums, SmallPrimes, Primes0),
    remove_one(Primes0, Primes),
    print_lines(Primes),
    halt.

read_input(M, N) :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [MTok, NTok | _],
    number_string(M, MTok),
    number_string(N, NTok).

primes_upto(Limit, Primes) :-
    (   Limit < 2
    ->  Primes = []
    ;   numlist(2, Limit, Nums),
        sieve_small(Nums, Limit, Primes)
    ).

sieve_small([], _, []).
sieve_small([P|Xs], Limit, [P|Ps]) :-
    (   P * P > Limit
    ->  Ps = Xs
    ;   filter_multiples(Xs, P, Ys),
        sieve_small(Ys, Limit, Ps)
    ).

filter_multiples([], _, []).
filter_multiples([X|Xs], P, Ys) :-
    (   X mod P =:= 0
    ->  filter_multiples(Xs, P, Ys)
    ;   Ys = [X|Rest],
        filter_multiples(Xs, P, Rest)
    ).

sieve_interval([], _, []).
sieve_interval(Nums, [], Nums).
sieve_interval(Nums, [P|Ps], Result) :-
    PP is P * P,
    filter_interval(Nums, P, PP, Nums1),
    sieve_interval(Nums1, Ps, Result).

filter_interval([], _, _, []).
filter_interval([X|Xs], P, PP, Ys) :-
    (   X < PP
    ->  Ys = [X|Rest],
        filter_interval(Xs, P, PP, Rest)
    ;   X mod P =:= 0
    ->  filter_interval(Xs, P, PP, Ys)
    ;   Ys = [X|Rest],
        filter_interval(Xs, P, PP, Rest)
    ).

remove_one([], []).
remove_one([1|Xs], Ys) :-
    remove_one(Xs, Ys).
remove_one([X|Xs], [X|Ys]) :-
    X =\= 1,
    remove_one(Xs, Ys).

print_lines([]).
print_lines([X|Xs]) :-
    write(X),
    nl,
    print_lines(Xs).