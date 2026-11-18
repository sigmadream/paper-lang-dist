:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   string_codes(Line, Codes),
        skip_ws(Codes, Codes1),
        parse_int(Codes1, M, Codes2),
        skip_ws(Codes2, Codes3),
        parse_int(Codes3, N, _),
        small_primes(1000, Primes),
        print_primes(M, N, Primes)
    ).

skip_ws([C|Cs], Rest) :-
    (   C =:= 32
    ;   C =:= 9
    ;   C =:= 10
    ;   C =:= 13
    ),
    !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

parse_int([C|Cs], V, Rest) :-
    C >= 0'0,
    C =< 0'9,
    !,
    V0 is C - 0'0,
    parse_digits(Cs, V0, V, Rest).

parse_digits([C|Cs], Acc, V, Rest) :-
    C >= 0'0,
    C =< 0'9,
    !,
    Acc1 is Acc * 10 + (C - 0'0),
    parse_digits(Cs, Acc1, V, Rest).
parse_digits(Rest, Acc, Acc, Rest).

small_primes(Limit, Primes) :-
    numlist(2, Limit, Ns),
    sieve(Ns, Primes).

sieve([], []).
sieve([P|Xs], [P|Ps]) :-
    remove_multiples(Xs, P, Rest),
    sieve(Rest, Ps).

remove_multiples([], _, []).
remove_multiples([X|Xs], P, Rest) :-
    (   X mod P =:= 0
    ->  Rest = Rest1
    ;   Rest = [X|Rest1]
    ),
    remove_multiples(Xs, P, Rest1).

print_primes(M, N, _) :-
    M > N,
    !.
print_primes(M, N, Primes) :-
    (   is_prime(M, Primes)
    ->  writeln(M)
    ;   true
    ),
    M1 is M + 1,
    print_primes(M1, N, Primes).

is_prime(N, _) :-
    N < 2,
    !,
    fail.
is_prime(N, Primes) :-
    is_prime_loop(N, Primes).

is_prime_loop(N, [P|Ps]) :-
    P * P =< N,
    !,
    (   N mod P =:= 0
    ->  fail
    ;   is_prime_loop(N, Ps)
    ).
is_prime_loop(_, _).