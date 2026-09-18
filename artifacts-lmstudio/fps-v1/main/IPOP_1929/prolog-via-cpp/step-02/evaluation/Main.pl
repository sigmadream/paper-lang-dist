:- use_module(library(lists)).

is_prime(2).
is_prime(N) :-
    N > 2,
    \+ (between(2, sqrt(N), D), N mod D =:= 0).

main :-
    read_line_to_string(_, Input),
    split_string(Input, ' ', '', [MStr, HStr]),
    M = MStr,
    H = HStr,
    between(M, H, N),
    is_prime(N),
    write(N), nl.