main :-
    read_int(N),
    Count is (1 << N) - 1,
    format("~d~n", [Count]),
    hanoi(N, 1, 2, 3).

hanoi(1, Start, _, End) :-
    format("~d ~d~n", [Start, End]).
hanoi(N, Start, Mid, End) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, Start, End, Mid),
    format("~d ~d~n", [Start, End]),
    hanoi(N1, Mid, Start, End).

read_int(N) :-
    get_code(C),
    skip_ws(C, C1),
    ( C1 =:= -1 ->
        N = 0
    ;
        read_digits(C1, 0, N)
    ).

skip_ws(C, C1) :-
    ( C =:= 32 ; C =:= 10 ; C =:= 9 ; C =:= 13 ) ->
        get_code(C2),
        skip_ws(C2, C1)
    ;
        C1 = C.

read_digits(C, Acc, N) :-
    ( C >= 48, C =< 57 ) ->
        D is C - 48,
        Acc1 is Acc * 10 + D,
        get_code(C1),
        read_digits(C1, Acc1, N)
    ;
        N = Acc.