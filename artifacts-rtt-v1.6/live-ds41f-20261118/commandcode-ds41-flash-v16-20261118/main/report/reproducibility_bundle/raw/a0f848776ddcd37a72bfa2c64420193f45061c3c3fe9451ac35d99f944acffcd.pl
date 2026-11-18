main :-
    read_line_to_string(user_input, Line0),
    (   Line0 == end_of_file
    ->  true
    ;   normalize_space(string(NStr), Line0),
        number_string(N, NStr),
        read_grid(N, Grid),
        solve(Grid, 0, 0, N, Result),
        format("~s~n", [Result])
    ).

read_grid(0, []) :- !.
read_grid(N, [Row|Rows]) :-
    N > 0,
    read_line_to_string(user_input, Row),
    N1 is N - 1,
    read_grid(N1, Rows).

solve(Grid, R, C, Size, Result) :-
    (   same_region(Grid, R, C, Size, Code)
    ->  string_codes(Result, [Code])
    ;   Half is Size // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(Grid, R, C, Half, TL),
        solve(Grid, R, C2, Half, TR),
        solve(Grid, R2, C, Half, BL),
        solve(Grid, R2, C2, Half, BR),
        string_concat("(", TL, S1),
        string_concat(S1, TR, S2),
        string_concat(S2, BL, S3),
        string_concat(S3, BR, S4),
        string_concat(S4, ")", Result)
    ).

same_region(Grid, R, C, Size, Code) :-
    nth0(R, Grid, Row),
    string_code(Row, C, Code),
    REnd is R + Size - 1,
    CEnd is C + Size - 1,
    rows_same(Grid, R, REnd, C, CEnd, Code).

rows_same(_, R, REnd, _, _, _) :-
    R > REnd,
    !.
rows_same(Grid, R, REnd, C, CEnd, Code) :-
    nth0(R, Grid, Row),
    cols_same(Row, C, CEnd, Code),
    R1 is R + 1,
    rows_same(Grid, R1, REnd, C, CEnd, Code).

cols_same(_, C, CEnd, _) :-
    C > CEnd,
    !.
cols_same(Row, C, CEnd, Code) :-
    string_code(Row, C, Code),
    C1 is C + 1,
    cols_same(Row, C1, CEnd, Code).