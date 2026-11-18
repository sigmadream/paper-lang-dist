main :-
    read(N),
    Count is (1 << N) - 1,
    writeln(Count),
    hanoi(N, 1, 2, 3).

hanoi(1, From, _Mid, To) :-
    format("~w ~w~n", [From, To]).
hanoi(N, From, Mid, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Mid),
    format("~w ~w~n", [From, To]),
    hanoi(N1, Mid, From, To).