:- use_module(library(pio)).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    split_string(Line, " ", " ", [M0, N0]),
    number_string(M, M0),
    number_string(N, N0),
    sieve(N, S),
    forall(between(M, N, I),
           (arg(I, S, 1) -> format("~d~n", [I]) ; true)).

sieve(N, S) :-
    functor(S, p, N),
    forall(between(1, N, I), setarg(I, S, 1)),
    setarg(1, S, 0),
    MaxI is floor(sqrt(N)),
    forall(between(2, MaxI, I),
           (arg(I, S, 1) -> mark_multiples(I, N, S) ; true)).

mark_multiples(I, N, S) :-
    Start is I * I,
    forall(between(Start, N, J, I), setarg(J, S, 0)).