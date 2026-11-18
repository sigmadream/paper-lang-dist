:- module(main, [main/0]).

hanoi(1, S, _, E) :- !,
    format("~d ~d~n", [S, E]).
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~d ~d~n", [S, E]),
    hanoi(N1, M, S, E).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file -> N = 0
    ;   split_string(Line, " \t\r\n", " \t\r\n", Parts),
        (   Parts == [] -> N = 0
        ;   Parts = [P|_],
            number_string(N, P)
        )
    ),
    (   N >= 1 ->
        C is (1 << N) - 1,
        format("~d~n", [C]),
        hanoi(N, 1, 2, 3)
    ;   true
    ).