main :-
    read_line_to_string(user_input, Line),
    number_string(N, Line),
    Count is (1 << N) - 1,
    format('~d~n', [Count]),
    hanoi(N, 1, 2, 3).

hanoi(1, From, _, To) :- !,
    format('~w ~w~n', [From, To]).
hanoi(N, From, Aux, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Aux),
    format('~w ~w~n', [From, To]),
    hanoi(N1, Aux, From, To).