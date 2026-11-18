:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Cs),
    (   Cs == end_of_file
    ->  N = 0
    ;   string_codes(Str, Cs),
        split_string(Str, " \t\r\n", "", Parts),
        (   Parts = [T|_], T \= ""
        ->  number_string(N, T)
        ;   N = 0
        )
    ),
    (   N >= 1
    ->  Cnt is 2^N - 1,
        format("~d~n", [Cnt]),
        hanoi(N, 1, 2, 3)
    ;   true
    ).

hanoi(1, S, _, E) :- !, format("~d ~d~n", [S, E]).
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~d ~d~n", [S, E]),
    hanoi(N1, M, S, E).