:- module(main, [main/0]).
:- use_module(library(charsio)).

main :-
    read_line_to_codes(user_input, NLine),
    ( NLine == end_of_file -> true
    ; number_codes(N, NLine),
      read_grid(N, Grid),
      solve(Grid, 0, 0, N, Codes),
      append(Codes, [0'\n], Out),
      put_chars(Out)
    ).

read_grid(0, []) :- !.
read_grid(N, [Row|Rows]) :-
    read_line_to_codes(user_input, Line),
    Line \== end_of_file,
    append(Row, [0'\n|Rest], Line), !,
    N1 is N - 1,
    read_grid(N1, Rest0),
    append(Rest0, [], Rest),
    Rows = Rest0.
read_grid(N, [Row|Rows]) :-
    read_line_to_codes(user_input, Line),
    Line \== end_of_file,
    append(Row, _, Line), !,
    N1 is N - 1,
    read_grid(N1, Rows).

solve(Grid, R, C, Size, Codes) :-
    get(Grid, R, C, First),
    ( all_same(Grid, R, C, Size, First)
    -> Codes = [First]
    ; Half is Size // 2,
      R1 is R + Half, C1 is C + Half,
      solve(Grid, R, C, Half, TL),
      solve(Grid, R, C1, Half, TR),
      solve(Grid, R1, C, Half, BL),
      solve(Grid, R1, C1, Half, BR),
      append([0'(|TL], T1),
      append(T1, TR, T2),
      append(T2, BL, T3),
      append(T3, BR, T4),
      append(T4, [0')], Codes)
    ).

all_same(_, _, _, 0, _) :- !.
all_same(Grid, R, C, Size, First) :-
    length(Row, Size),
    nth0(R, Grid, Row),
    append(Prefix, [First|Rest], Row),
    length(Prefix, C),
    !,
    Rest = [],
    Size1 is Size - 1,
    R1 is R + 1,
    all_same(Grid, R1, C, Size1, First).

get(Grid, R, C, X) :-
    nth0(R, Grid, Row),
    nth0(C, Row, X).

put_chars([]).
put_chars([H|T]) :- put_code(H), put_chars(T).