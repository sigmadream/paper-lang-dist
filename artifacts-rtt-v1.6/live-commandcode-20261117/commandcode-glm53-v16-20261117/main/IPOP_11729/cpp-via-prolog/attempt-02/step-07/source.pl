:- module(main, [main/0]).
:- use_module(library(charsio)).
:- use_module(library(lists)).
:- use_module(library(pipes)).

main :-
    current_input(In),
    read_line_to_chars(In, Line0),
    ( Line0 == end_of_file -> true
    ; atom_number(Line0, N0)
    ->  ( N0 < 1 -> true
        ;  M is (1 << N0) - 1,
           format("~d~n", [M]),
           hanoi(N0, 1, 2, 3)
        )
    ;   true
    ).

hanoi(1, A, _, C) :- !, format("~d ~d~n", [A, C]).
hanoi(N, A, B, C) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, A, C, B),
    format("~d ~d~n", [A, C]),
    hanoi(N1, B, A, C).