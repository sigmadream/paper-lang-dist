:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\n\r", " \t\n\r", [Ms, Ns | _]),
    number_string(M, Ms),
    number_string(N, Ns),
    ( M < 2 -> Start = 2 ; Start = M ),
    ( Start =< N ->
        Limit is floor(sqrt(N)) + 1,
        small_primes(Limit, AllPs),
        ( Start =< 2, 2 =< N -> writeln(2) ; true ),
        S1 is max(Start, 3),
        ( S1 mod 2 =:= 0 -> S2 is S1 + 1 ; S2 = S1 ),
        ( AllPs = [2|OddPs] -> true ; OddPs = [] ),
        print_odds(S2, N, OddPs)
    ; true
    ).

small_primes(Limit, Ps) :-
    range(2, Limit, L),
    sieve(L, Ps).

range(L, H, []) :- L > H, !.
range(L, H, [L|T]) :- L2 is L + 1, range(L2, H, T).

sieve([], []).
sieve([P|Xs], [P|Ps]) :-
    remove_multiples(P, Xs, R),
    sieve(R, Ps).

remove_multiples(_, [], []).
remove_multiples(P, [X|Xs], R) :-
    ( X mod P =:= 0 ->
        R = R1
    ;   R = [X|R1]
    ),
    remove_multiples(P, Xs, R1).

print_odds(I, N, _) :- I > N, !.
print_odds(I, N, Ps) :-
    ( is_prime_odd(I, Ps) -> writeln(I) ; true ),
    I1 is I + 2,
    print_odds(I1, N, Ps).

is_prime_odd(I, [P|Ps]) :-
    ( P * P > I ->
        true
    ; I mod P =:= 0 ->
        false
    ; is_prime_odd(I, Ps)
    ).
is_prime_odd(_, []) :- true.