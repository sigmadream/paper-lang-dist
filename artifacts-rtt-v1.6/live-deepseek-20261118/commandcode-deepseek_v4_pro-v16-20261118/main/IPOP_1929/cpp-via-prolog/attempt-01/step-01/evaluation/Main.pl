:- module(main, [main/0]).

main :-
    read_line_to_string(user_input, Line),
    ( Line = end_of_file -> halt ; true ),
    split_string(Line, " ", " ", [MStr,NStr]),
    number_string(M, MStr),
    number_string(N, NStr),
    ( N >= 2 -> numlist(2, N, L) ; L = [] ),
    sieve(L, N, Primes),
    forall(member(P, Primes), ( P >= M -> (write(P), nl) ; true )).

sieve([], _, []).
sieve([P|Rest], N, [P|Primes]) :-
    ( P*P > N -> Primes = Rest
    ; exclude(multiple(P), Rest, NewRest),
      sieve(NewRest, N, Primes)
    ).

multiple(P, X) :- 0 is X mod P.