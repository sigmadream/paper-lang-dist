read_int(N) :-
    get_code(C),
    (   C =:= -1
    ->  N = 0
    ;   C >= 48, C =< 57
    ->  read_number(C, N)
    ;   read_int(N)
    ).

read_number(C, N) :-
    Acc0 is C - 48,
    read_number_rest(Acc0, N).

read_number_rest(Acc, N) :-
    get_code(C),
    (   C >= 48, C =< 57
    ->  Acc1 is Acc * 10 + (C - 48),
        read_number_rest(Acc1, N)
    ;   N = Acc
    ).

hanoi(1, From, _, To) :-
    !,
    format('~d ~d~n', [From, To]).
hanoi(N, From, By, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, By),
    format('~d ~d~n', [From, To]),
    hanoi(N1, By, From, To).

main :-
    read_int(N),
    (   N > 0
    ->  Moves is (1 << N) - 1,
        format('~d~n', [Moves]),
        hanoi(N, 1, 2, 3)
    ;   true
    ),
    flush_output.