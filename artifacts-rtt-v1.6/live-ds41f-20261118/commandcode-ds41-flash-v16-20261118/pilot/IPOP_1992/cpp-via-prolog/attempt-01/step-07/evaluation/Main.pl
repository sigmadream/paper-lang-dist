clean_codes([], []).
clean_codes([C|Cs], Out) :-
    (C =:= 10 ; C =:= 13),
    !,
    clean_codes(Cs, Out).
clean_codes([C|Cs], [C|Out]) :-
    clean_codes(Cs, Out).

read_rows(0, []) :- !.
read_rows(N, [Row|Rest]) :-
    read_line_to_codes(user_input, Codes),
    Codes \== end_of_file,
    clean_codes(Codes, Row),
    N1 is N - 1,
    read_rows(N1, Rest).

same_cols(J, EndC, _, _) :-
    J >= EndC,
    !.
same_cols(J, EndC, Row, V) :-
    nth0(J, Row, X),
    X == V,
    J1 is J + 1,
    same_cols(J1, EndC, Row, V).

same_rows(I, EndR, _, _, _, _) :-
    I >= EndR,
    !.
same_rows(I, EndR, C, EndC, Grid, V) :-
    nth0(I, Grid, Row),
    same_cols(C, EndC, Row, V),
    I1 is I + 1,
    same_rows(I1, EndR, C, EndC, Grid, V).

same_region(R, C, Size, Grid, V) :-
    EndR is R + Size,
    EndC is C + Size,
    same_rows(R, EndR, C, EndC, Grid, V).

solve(R, C, Size, Grid, Codes) :-
    nth0(R, Grid, Row),
    nth0(C, Row, V),
    (   same_region(R, C, Size, Grid, V)
    ->  Codes = [V]
    ;   Half is Size // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(R, C, Half, Grid, TL),
        solve(R, C2, Half, Grid, TR),
        solve(R2, C, Half, Grid, BL),
        solve(R2, C2, Half, Grid, BR),
        append([[40], TL, TR, BL, BR, [41]], Codes)
    ).

main :-
    read_line_to_codes(user_input, NCodes0),
    NCodes0 \== end_of_file,
    clean_codes(NCodes0, NCodes),
    number_codes(N, NCodes),
    read_rows(N, Grid),
    solve(0, 0, N, Grid, Codes),
    format('~s~n', [Codes]).