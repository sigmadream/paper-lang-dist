:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", [MStr, NStr]),
    number_string(M, MStr),
    number_string(N, NStr),
    N1 is N + 1,
    length(FlagsList, N1),
    fill_ones(FlagsList),
    Flags =.. [flags|FlagsList],
    setarg(1, Flags, 0),
    ( N >= 1 -> setarg(2, Flags, 0) ; true ),
    sieve(2, N, Flags),
    print_primes(M, N, Flags).

fill_ones([]).
fill_ones([1|T]) :-
    fill_ones(T).

sieve(P, N, _) :-
    P * P > N,
    !.
sieve(P, N, Flags) :-
    Idx is P + 1,
    arg(Idx, Flags, V),
    ( V =:= 1 -> mark(P, N, Flags) ; true ),
    P1 is P + 1,
    sieve(P1, N, Flags).

mark(P, N, Flags) :-
    Start is P * P,
    mark_loop(Start, P, N, Flags).

mark_loop(J, _, N, _) :-
    J > N,
    !.
mark_loop(J, P, N, Flags) :-
    Idx is J + 1,
    setarg(Idx, Flags, 0),
    J1 is J + P,
    mark_loop(J1, P, N, Flags).

print_primes(I, N, _) :-
    I > N,
    !.
print_primes(I, N, Flags) :-
    Idx is I + 1,
    arg(Idx, Flags, V),
    ( V =:= 1 -> format("~d~n", [I]) ; true ),
    I1 is I + 1,
    print_primes(I1, N, Flags).