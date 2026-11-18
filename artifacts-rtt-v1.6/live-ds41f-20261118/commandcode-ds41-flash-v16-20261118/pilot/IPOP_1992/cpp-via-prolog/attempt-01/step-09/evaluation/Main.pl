main :-
    read_line_to_string(user_input, First),
    (   First == end_of_file
    ->  true
    ;   parse_int_line(First, N),
        read_grid(N, Rows),
        maplist(string_chars, Rows, Grid),
        solve(0, 0, N, Grid, Result),
        format("~s~n", [Result])
    ).

parse_int_line(Str, N) :-
    split_string(Str, " \t\r\n", " \t\r\n", Parts),
    Parts = [P|_],
    number_string(N, P).

read_grid(0, []) :- !.
read_grid(N, [Line|Lines]) :-
    N > 0,
    read_line_to_string(user_input, Line),
    N1 is N - 1,
    read_grid(N1, Lines).

solve(R, C, Size, Grid, Result) :-
    nth0(R, Grid, Row),
    nth0(C, Row, V),
    (   same_region(R, C, Size, Grid, V)
    ->  string_chars(Result, [V])
    ;   Half is Size // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(R, C, Half, Grid, A),
        solve(R, C2, Half, Grid, B),
        solve(R2, C, Half, Grid, D),
        solve(R2, C2, Half, Grid, E),
        string_concat("(", A, T1),
        string_concat(T1, B, T2),
        string_concat(T2, D, T3),
        string_concat(T3, E, T4),
        string_concat(T4, ")", Result)
    ).

same_region(R, C, Size, Grid, V) :-
    REnd is R + Size,
    CEnd is C + Size,
    same_rows(R, REnd, C, CEnd, Grid, V).

same_rows(R, REnd, _, _, _, _) :-
    R >= REnd, !.
same_rows(R, REnd, C, CEnd, Grid, V) :-
    nth0(R, Grid, Row),
    same_cols(Row, C, CEnd, V),
    R1 is R + 1,
    same_rows(R1, REnd, C, CEnd, Grid, V).

same_cols(_, C, CEnd, _) :-
    C >= CEnd, !.
same_cols(Row, C, CEnd, V) :-
    nth0(C, Row, X),
    X == V,
    C1 is C + 1,
    same_cols(Row, C1, CEnd, V).