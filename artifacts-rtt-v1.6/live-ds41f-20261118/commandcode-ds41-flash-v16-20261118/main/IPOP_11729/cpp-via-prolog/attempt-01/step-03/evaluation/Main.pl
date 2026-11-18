main :-
    ( read_int(N) ->
        Count is (1 << N) - 1,
        writeln(Count),
        hanoi(N, 1, 2, 3),
        flush_output
    ; true
    ).

read_int(N) :-
    get_code(C),
    skip_ws(C, C1),
    C1 =\= -1,
    read_digits(C1, 0, N).

skip_ws(-1, -1) :- !.
skip_ws(C, C) :-
    C =\= 32,
    C =\= 10,
    C =\= 13,
    C =\= 9,
    !.
skip_ws(_, C1) :-
    get_code(C),
    skip_ws(C, C1).

read_digits(C, Acc, N) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + C - 48,
    get_code(C1),
    ( C1 >= 48, C1 =< 57 ->
        read_digits(C1, Acc1, N)
    ; N = Acc1
    ).
read_digits(_, Acc, Acc).

hanoi(1, S, _, E) :-
    !,
    format("~d ~d~n", [S, E]).
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~d ~d~n", [S, E]),
    hanoi(N1, M, S, E).