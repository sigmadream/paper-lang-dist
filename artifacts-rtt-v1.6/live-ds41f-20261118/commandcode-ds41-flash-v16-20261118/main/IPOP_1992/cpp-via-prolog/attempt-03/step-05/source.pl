main :-
    read_line_to_string(user_input, LineN0),
    ( LineN0 == end_of_file ->
        true
    ;
        strip_cr(LineN0, LineN),
        number_string(N, LineN),
        read_rows(N, Grid),
        solve(Grid, 0, 0, N, Result),
        format("~s~n", [Result])
    ).

strip_cr(S0, S) :-
    ( string_concat(S, "\r", S0) ->
        true
    ;
        S = S0
    ).

read_rows(0, []) :- !.
read_rows(N, [Row|Rows]) :-
    N > 0,
    read_line_to_string(user_input, Row0),
    ( Row0 == end_of_file ->
        Row = ""
    ;
        strip_cr(Row0, Row)
    ),
    N1 is N - 1,
    read_rows(N1, Rows).

solve(Grid, R, C, Size, Result) :-
    nth0(R, Grid, RowR),
    string_code(RowR, C, Value),
    ( all_same(Grid, R, C, Size, Value) ->
        char_code(Ch, Value),
        atom_string(Ch, Result)
    ;
        Half is Size // 2,
        solve(Grid, R, C, Half, S1),
        C2 is C + Half,
        solve(Grid, R, C2, Half, S2),
        R2 is R + Half,
        solve(Grid, R2, C, Half, S3),
        solve(Grid, R2, C2, Half, S4),
        string_concat("(", S1, T1),
        string_concat(T1, S2, T2),
        string_concat(T2, S3, T3),
        string_concat(T3, S4, T4),
        string_concat(T4, ")", Result)
    ).

all_same(Grid, R, C, Size, Value) :-
    REnd is R + Size,
    CEnd is C + Size,
    all_rows(Grid, R, REnd, C, CEnd, Value).

all_rows(_, I, IEnd, _, _, _) :-
    I >= IEnd.
all_rows(Grid, I, IEnd, C, CEnd, Value) :-
    I < IEnd,
    nth0(I, Grid, Row),
    all_cols(Row, C, CEnd, Value),
    I1 is I + 1,
    all_rows(Grid, I1, IEnd, C, CEnd, Value).

all_cols(_, J, JEnd, _) :-
    J >= JEnd.
all_cols(Row, J, JEnd, Value) :-
    J < JEnd,
    string_code(Row, J, Code),
    Code =:= Value,
    J1 is J + 1,
    all_cols(Row, J1, JEnd, Value).