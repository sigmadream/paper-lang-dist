main :-
    read_line_to_string(user_input, LineN),
    (   LineN == end_of_file
    ->  true
    ;   number_string(N, LineN),
        read_grid(N, [], GridRev),
        reverse(GridRev, Grid),
        solve(Grid, 0, 0, N, Result),
        format("~s~n", [Result])
    ).

read_grid(0, Acc, Acc) :- !.
read_grid(N, Acc, Grid) :-
    N > 0,
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  fail
    ;   string_chars(Line, Chars),
        N1 is N - 1,
        read_grid(N1, [Chars|Acc], Grid)
    ).

get_char(Grid, R, C, Ch) :-
    nth0(R, Grid, Row),
    nth0(C, Row, Ch).

all_same(Grid, R, C, Size, First) :-
    get_char(Grid, R, C, First),
    EndR is R + Size - 1,
    EndC is C + Size - 1,
    all_same_rows(Grid, R, C, EndR, EndC, First).

all_same_rows(_, R, _, EndR, _, _) :- R > EndR, !.
all_same_rows(Grid, R, C, EndR, EndC, First) :-
    all_same_cols(Grid, R, C, EndC, First),
    R1 is R + 1,
    all_same_rows(Grid, R1, C, EndR, EndC, First).

all_same_cols(_, _, C, EndC, _) :- C > EndC, !.
all_same_cols(Grid, R, C, EndC, First) :-
    get_char(Grid, R, C, Ch),
    Ch == First,
    C1 is C + 1,
    all_same_cols(Grid, R, C1, EndC, First).

solve(Grid, R, C, Size, Result) :-
    (   Size = 1
    ->  get_char(Grid, R, C, Result)
    ;   all_same(Grid, R, C, Size, First)
    ->  Result = First
    ;   Half is Size // 2,
        R1 is R,          C1 is C,
        R2 is R,          C2 is C + Half,
        R3 is R + Half,   C3 is C,
        R4 is R + Half,   C4 is C + Half,
        solve(Grid, R1, C1, Half, TL),
        solve(Grid, R2, C2, Half, TR),
        solve(Grid, R3, C3, Half, BL),
        solve(Grid, R4, C4, Half, BR),
        atom_concat('(', TL, Temp1),
        atom_concat(Temp1, TR, Temp2),
        atom_concat(Temp2, BL, Temp3),
        atom_concat(Temp3, BR, Temp4),
        atom_concat(Temp4, ')', Result)
    ).