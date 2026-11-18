digits([], []).
digits([C|Cs], [C|Ds]) :-
    C >= 48, C =< 57, !,
    digits(Cs, Ds).
digits([_|Cs], Ds) :-
    digits(Cs, Ds).

bits([], []).
bits([C|Cs], [C|Ds]) :-
    (C =:= 48 ; C =:= 49), !,
    bits(Cs, Ds).
bits([_|Cs], Ds) :-
    bits(Cs, Ds).

read_grid(0, []) :- !.
read_grid(N, Grid) :-
    N > 0,
    read_line_to_codes(user_input, Codes),
    bits(Codes, Row),
    ( Row == [] ->
        read_grid(N, Grid)
    ;   N1 is N - 1,
        Grid = [Row|Rest],
        read_grid(N1, Rest)
    ).

all_same(Grid, R, C, Size, V) :-
    REnd is R + Size - 1,
    CEnd is C + Size - 1,
    forall(
        (between(R, REnd, I), between(C, CEnd, J)),
        (nth0(I, Grid, Row), nth0(J, Row, Cell), Cell = V)
    ).

solve(Grid, R, C, Size, Codes) :-
    nth0(R, Grid, Row),
    nth0(C, Row, V),
    ( all_same(Grid, R, C, Size, V) ->
        Codes = [V]
    ;   Half is Size // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(Grid, R, C, Half, TL),
        solve(Grid, R, C2, Half, TR),
        solve(Grid, R2, C, Half, BL),
        solve(Grid, R2, C2, Half, BR),
        append([40|TL], TR, T1),
        append(T1, BL, T2),
        append(T2, BR, T3),
        append(T3, [41], Codes)
    ).

main :-
    read_line_to_codes(user_input, Line),
    digits(Line, Digits),
    number_codes(N, Digits),
    read_grid(N, Grid),
    solve(Grid, 0, 0, N, Codes),
    format("~s~n", [Codes]).