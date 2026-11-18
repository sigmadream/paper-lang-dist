main :-
    (   read_line_to_codes(user_input, Codes),
        Codes \== end_of_file
    ->  number_codes(N, Codes),
        Count is (1 << N) - 1,
        format('~d~n', [Count]),
        hanoi(N, 1, 2, 3)
    ;   true
    ).

hanoi(1, A, _, C) :- !,
    format('~w ~w~n', [A, C]).
hanoi(N, A, B, C) :-
    N1 is N - 1,
    hanoi(N1, A, C, B),
    format('~w ~w~n', [A, C]),
    hanoi(N1, B, A, C).