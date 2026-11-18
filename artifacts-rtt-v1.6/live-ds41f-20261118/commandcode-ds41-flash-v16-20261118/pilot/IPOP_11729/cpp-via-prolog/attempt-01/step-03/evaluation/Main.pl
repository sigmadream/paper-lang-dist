main :-
    read_line_to_codes(user_input, Codes),
    number_codes(N, Codes),
    Moves is (1 << N) - 1,
    format("~w~n", [Moves]),
    hanoi(N, 1, 2, 3).

hanoi(1, S, _, E) :-
    format("~w ~w~n", [S, E]).
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~w ~w~n", [S, E]),
    hanoi(N1, M, S, E).