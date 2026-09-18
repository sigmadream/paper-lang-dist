:- use_module(library(lists)).

main :-
    read_line_to_string(user_input, Input),
    split_string(Input, " ", "", [MStr, NStr]),
    M = MStr,
    N = NStr,
    findall(X, (between(M, N, X), prime(X)), Primes),
    maplist(writeLn, Primes).

prime(2).
prime(X) :-
    X > 2,
    \+ (between(2, sqrt(X), Y), X mod Y =:= 0).

writeLn(X) :-
    write(X),
    nl.