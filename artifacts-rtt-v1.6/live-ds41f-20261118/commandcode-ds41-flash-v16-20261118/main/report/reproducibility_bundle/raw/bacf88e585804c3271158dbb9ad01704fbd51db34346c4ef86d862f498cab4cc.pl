read_int(N) :-
    get_code(C),
    read_int_start(C, N).

read_int_start(C, N) :-
    ( C =:= -1 -> N = 0
    ; C >= 48, C =< 57 -> N0 is C - 48, read_int_digits(N0, N)
    ; read_int(N)
    ).

read_int_digits(Acc, N) :-
    get_code(C),
    ( C >= 48, C =< 57 ->
        Acc1 is Acc * 10 + (C - 48),
        read_int_digits(Acc1, N)
    ; N = Acc
    ).

main :-
    read_int(N),
    N > 0,
    Full is (1 << N) - 1,
    count_queens(0, N, Full, 0, 0, 0, Count),
    format("~w~n", [Count]).

count_queens(R, N, _, _, _, _, 1) :-
    R =:= N,
    !.
count_queens(R, N, Full, Cols, A, B, Count) :-
    R < N,
    Avail is Full - (Cols \/ A \/ B),
    count_avail(Avail, R, N, Full, Cols, A, B, Count).

count_avail(0, _, _, _, _, _, _, 0) :-
    !.
count_avail(Avail, R, N, Full, Cols, A, B, Count) :-
    Avail > 0,
    Bit is Avail /\ -Avail,
    NewCols is Cols \/ Bit,
    NewA is (A \/ Bit) >> 1,
    NewB is ((B \/ Bit) << 1) /\ Full,
    R1 is R + 1,
    count_queens(R1, N, Full, NewCols, NewA, NewB, C1),
    Rest is Avail - Bit,
    count_avail(Rest, R, N, Full, Cols, A, B, C2),
    Count is C1 + C2.