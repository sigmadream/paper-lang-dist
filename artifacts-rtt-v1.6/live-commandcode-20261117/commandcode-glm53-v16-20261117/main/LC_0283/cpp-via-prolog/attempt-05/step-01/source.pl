:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    current_input(In),
    read_line_to_string(In, Line1),
    read_line_to_string(In, Line2),
    number_string(N, Line1),
    split_string(Line2, " ", "\s\t\r\n", Parts),
    maplist(number_string, Nums0, Parts),
    length(Nums0, N),
    partition_moves(Nums0, NonZeros, Zeros),
    append(NonZeros, Zeros, Result),
    maplist(term_string, Result, Strs),
    atomic_list_concat(Strs, " ", Joined),
    write(Joined), nl.

partition_moves([], [], []).
partition_moves([X|Xs], [X|Nz], Z) :- X =\= 0, !, partition_moves(Xs, Nz, Z).
partition_moves([X|Xs], Nz, [X|Z]) :- partition_moves(Xs, Nz, Z).