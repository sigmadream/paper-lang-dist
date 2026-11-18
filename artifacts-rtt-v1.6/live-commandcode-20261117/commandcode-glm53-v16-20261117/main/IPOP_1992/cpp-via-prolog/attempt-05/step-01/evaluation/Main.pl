:- module(main, [main/0]).
:- use_module(library(readutil)).

read_int(Stream, N) :-
    read_line_to_codes(Stream, Line),
    (Line == end_of_file -> N = 0
    ; line_number(Line, N)).

line_number(Codes, N) :-
    number_codes(N, Codes).

read_grid(_, 0, []).
read_grid(Stream, N, [Row|Rows]) :-
    read_line_to_codes(Stream, Line),
    Line \== end_of_file,
    length(Row, N),
    maplist(digit_code, Row),
    N1 is N - 1,
    read_grid(Stream, N1, Rows).

digit_code(C) :- C =:= 48 ; C =:= 49.

same_value([Row|Rows], C, R, S) :-
    nth0(R, [Row|Rows], Line),
    sub_string(Line, C, S, _, Sub),
    string_chars(Sub, Chars),
    maplist([X]>>(X == Chars), Chars).

% check uniform block
uniform(Grid, R, C, S, Ch) :-
    nth0(R, Grid, Row),
    string_chars(Row, RowChars),
    nth0(C, RowChars, Ch),
    check_all(Grid, R, C, S, Ch).

check_all(_, R, _, S, _) :- R >= S, !.
check_all(Grid, R, C, S, Ch) :-
    nth0(R, Grid, Row),
    string_chars(Row, RowChars),
    check_row(RowChars, C, S, Ch),
    R1 is R + 1,
    check_all(Grid, R1, C, S, Ch).

check_row(_, C, _, Ch) :- C >= _, fail.
check_row(_, _, S, _) :- S =< 0, !.
check_row(RowChars, C, S, Ch) :-
    nth0(C, RowChars, X),
    X == Ch,
    C1 is C + 1,
    S1 is S - 1,
    check_row(RowChars, C1, S1, Ch).

solve(Grid, R, C, S, Result) :-
    (   uniform(Grid, R, C, S, Ch)
    ->  atom_chars(Result, [Ch])
    ;   H is S // 2,
        R1 is R, C1 is C,
        R2 is R, C2 is C + H,
        R3 is R + H, C3 is C,
        R4 is R + H, C4 is C + H,
        solve(Grid, R1, C1, H, A),
        solve(Grid, R2, C2, H, B),
        solve(Grid, R3, C3, H, Cc),
        solve(Grid, R4, C4, H, D),
        atomic_list_concat(['(', A, B, Cc, D, ')'], Result)
    ).

main :-
    current_input(Stream),
    read_int(Stream, N),
    (   N > 0
    ->  read_grid(Stream, N, N, Grid),
        solve(Grid, 0, 0, N, Result),
        write(Result), nl
    ;   true
    ).