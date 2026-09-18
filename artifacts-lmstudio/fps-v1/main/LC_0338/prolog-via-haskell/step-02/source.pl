:- module(main, [main/0]).
:- use_module(library(io)).

count_bits(N, Counts) :-
    findall(C, (between(0, N, I), C is bit_count(I)), Counts).

bit_count(X) :-
    X < 2, !,
    X.
bit_count(X) :-
    Y is X // 2,
    Z is X mod 2,
    bit_count(Y, YZ),
    Z =:= 1 -> YZ + 1; YZ.

main :-
    read_line_to_string(_, Input),
    atom_number(Input, N),
    count_bits(N, Counts),
    maplist(write, Counts),
    write('\n').