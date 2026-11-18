main :-
    read_line_to_string(user_input, NLine),
    (   NLine == end_of_file
    ->  true
    ;   number_string(N, NLine),
        read_rows(N, Rows),
        solve(Rows, 0, 0, N, Code),
        format('~s~n', [Code])
    ).

read_rows(0, []) :- !.
read_rows(N, [Row|Rest]) :-
    read_line_to_string(user_input, Row),
    N1 is N - 1,
    read_rows(N1, Rest).

solve(Rows, R, C, Size, Code) :-
    nth0(R, Rows, Row),
    string_code(Row, C, First),
    (   all_same(Rows, R, C, Size, First)
    ->  string_codes(Code, [First])
    ;   Half is Size // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(Rows, R, C, Half, TL),
        solve(Rows, R, C2, Half, TR),
        solve(Rows, R2, C, Half, BL),
        solve(Rows, R2, C2, Half, BR),
        string_concat("(", TL, A),
        string_concat(A, TR, B),
        string_concat(B, BL, C1),
        string_concat(C1, BR, D),
        string_concat(D, ")", Code)
    ).

all_same(Rows, R, C, Size, First) :-
    REnd is R + Size,
    CEnd is C + Size,
    all_same_loop(Rows, R, C, REnd, CEnd, First).

all_same_loop(_, R, _, REnd, _, _) :-
    R >= REnd,
    !.
all_same_loop(Rows, R, C, REnd, CEnd, First) :-
    nth0(R, Rows, Row),
    check_row(Row, C, CEnd, First),
    R1 is R + 1,
    all_same_loop(Rows, R1, C, REnd, CEnd, First).

check_row(_, C, CEnd, _) :-
    C >= CEnd,
    !.
check_row(Row, C, CEnd, First) :-
    string_code(Row, C, First),
    C1 is C + 1,
    check_row(Row, C1, CEnd, First).