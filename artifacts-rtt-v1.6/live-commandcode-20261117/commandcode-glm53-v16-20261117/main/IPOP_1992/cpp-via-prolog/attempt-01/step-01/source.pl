:- module(main, [main/0]).
:- use_module(library(readutil)).

read_grid(N, Grid) :-
    read_grid_lines(N, Lines),
    maplist(atom_chars, Lines, Grid).

read_grid_lines(0, []).
read_grid_lines(N, [L|Ls]) :-
    N > 0,
    read_line_to_string(current_input, S),
    ( S == end_of_file -> L = ''
    ; string_chars(S, Chars),
      exclude([C]>>(C == '\n' ; C == '\r' ; C == ' '), Chars, FChars),
      atom_chars(L, FChars)
    ),
    N1 is N - 1,
    read_grid_lines(N1, Ls).

all_same([[C|Rest]|Rows], C) :-
    row_same(Rest, C),
    rows_same(Rows, C).

row_same([], _).
row_same([C|Cs], C) :- row_same(Cs, C).

rows_same([], _).
rows_same([Row|Rows], C) :- row_same(Row, C), rows_same(Rows, C).

solve(_, _, _, 0, "") :- !.
solve(Grid, R, C, Size, Out) :-
    length(Grid, N),
    between(0, N, R),
    between(0, N, C),
    Size > 0,
    sub_region(Grid, R, Size, Rows),
    maplist([Row, Sub]>>(length(Sub, Size), append(_, Sub2, Row), append(Sub, _, Sub2)), Rows, Region),
    ( all_same(Region, First) ->
        atom_chars(Out, [First])
    ; Half is Size // 2,
      R1 is R, C1 is C, R2 is R + Half, C2 is C + Half,
      solve(Grid, R1, C1, Half, TL),
      solve(Grid, R1, C2, Half, TR),
      solve(Grid, R2, C1, Half, BL),
      solve(Grid, R2, C2, Half, BR),
      format(string(S), "(~w~w~w~w)", [TL, TR, BL, BR]),
      Out = S
    ).

sub_region(_, _, 0, []).
sub_region(Grid, R, Size, [Row|Rows]) :-
    Size > 0,
    nth0(R, Grid, Row),
    R1 is R + 1,
    Size1 is Size - 1,
    sub_region(Grid, R1, Size1, Rows).

main :-
    read_line_to_string(current_input, Line1),
    Line1 \== end_of_file,
    split_string(Line1, " \t\r\n", " \t\r\n", [NAtom|_]),
    atom_number(NAtom, N),
    read_grid(N, Grid),
    solve(Grid, 0, 0, N, Out),
    write(Out), nl,
    !.
main.