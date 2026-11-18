main :-
    read_number(N),
    count_solutions(N, Count),
    writeln(Count).

read_number(N) :-
    get_code(C),
    read_number_chars(C, Codes),
    number_codes(N, Codes).

read_number_chars(-1, []) :- !.
read_number_chars(C, Codes) :-
    (   C =:= 10 -> Codes = []
    ;   C =:= 13 ->
        get_code(C1),
        read_number_chars(C1, Codes)
    ;   C =:= 32 ->
        get_code(C1),
        read_number_chars(C1, Codes)
    ;   C =:= 9 ->
        get_code(C1),
        read_number_chars(C1, Codes)
    ;   Codes = [C|Rest],
        get_code(C1),
        read_number_chars(C1, Rest)
    ).

count_solutions(N, Count) :-
    All is (1 << N) - 1,
    count_queens(0, N, All, 0, 0, 0, Count).

count_queens(R, N, All, Cols, D1, D2, Count) :-
    (   R =:= N -> Count = 1
    ;   Used is Cols \/ D1 \/ D2,
        Available is All /\ \ (Cols \/ D1 \/ D2),
        count_bits(Available, R, N, All, Cols, D1, D2, Count)
    ).

count_bits(Avail, R, N, All, Cols, D1, D2, Count) :-
    (   Avail =:= 0 -> Count = 0
    ;   B is Avail /\ -Avail,
        Rest is Avail /\ (Avail - 1),
        NewCols is Cols \/ B,
        NewD1 is (D1 \/ B) << 1,
        NewD2 is (D2 \/ B) >> 1,
        R1 is R + 1,
        count_queens(R1, N, All, NewCols, NewD1, NewD2, C1),
        count_bits(Rest, R, N, All, Cols, D1, D2, C2),
        Count is C1 + C2
    ).