:- module(main, [main/0]).

:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line1),
    Line1 \= end_of_file,
    number_string(N, Line1),
    read_grid(N, Grid),
    solve(Grid, 0, 0, N, Encoded),
    format("~s~n", [Encoded]).

read_grid(0, []) :- !.
read_grid(N, [Row|Rest]) :-
    N > 0,
    read_line_to_string(user_input, Line),
    Line \= end_of_file,
    string_chars(Line, Row),
    N1 is N - 1,
    read_grid(N1, Rest).

all_same(Grid, R, C, Size, First) :-
    EndR is R + Size - 1,
    EndC is C + Size - 1,
    forall((
        between(R, EndR, I),
        between(C, EndC, J),
        nth0(I, Grid, Row),
        nth0(J, Row, Ch)
    ), Ch == First).

solve(Grid, R, C, Size, Encoded) :-
    nth0(R, Grid, Row),
    nth0(C, Row, First),
    (   all_same(Grid, R, C, Size, First)
    ->  atom_chars(Encoded, [First])
    ;   Half is Size // 2,
        solve(Grid, R, C, Half, TL),
        R2 is R,
        C2 is C + Half,
        solve(Grid, R2, C2, Half, TR),
        R3 is R + Half,
        C3 is C,
        solve(Grid, R3, C3, Half, BL),
        R4 is R + Half,
        C4 is C + Half,
        solve(Grid, R4, C4, Half, BR),
        atom_concat('(', TL, Tmp1),
        atom_concat(Tmp1, TR, Tmp2),
        atom_concat(Tmp2, BL, Tmp3),
        atom_concat(Tmp3, BR, Tmp4),
        atom_concat(Tmp4, ')', Encoded)
    ).