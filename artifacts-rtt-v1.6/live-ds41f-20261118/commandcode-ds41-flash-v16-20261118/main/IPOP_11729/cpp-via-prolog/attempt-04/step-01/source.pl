main :-
    ( catch(read(N), _, fail), integer(N) ->
        Count is (1 << N) - 1,
        format("~d~n", [Count]),
        hanoi(N, 1, 2, 3)
    ; true
    ).

hanoi(1, S, _, E) :- !, format("~d ~d~n", [S, E]).
hanoi(N, S, M, E) :-
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~d ~d~n", [S, E]),
    hanoi(N1, M, S, E).