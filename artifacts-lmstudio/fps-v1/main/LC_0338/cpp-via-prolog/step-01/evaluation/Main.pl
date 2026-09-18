:- use_module(library(io)).

main :-
    read_line_to_string(Input),
    string_to_integer(Input, N),
    findall(C, count_bits(N, C), Counts),
    maplist(write, Counts),
    nl.

count_bits(0, 0).
count_bits(N, C) :-
    N1 is N // 2,
    count_bits(N1, C1),
    C is C1 + (N mod 2).