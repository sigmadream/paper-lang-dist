:- module(main, [main/0]).

read_grid(0, []).
read_grid(N, [Row|Rest]) :-
    N > 0,
    read_line_to_string(user_input, Line),
    string_chars(Line, Row),
    N1 is N - 1,
    read_grid(N1, Rest).

get_char(Grid, R, C, Char) :-
    nth0(R, Grid, RowList),
    nth0(C, RowList, Char).

all_same(Grid, R, C, Size, Char) :-
    get_char(Grid, R, C, Char),
    Rmax is R + Size - 1,
    Cmax is C + Size - 1,
    forall(between(R, Rmax, I),
           forall(between(C, Cmax, J),
                  get_char(Grid, I, J, Char))).

solve(Grid, R, C, Size, Result) :-
    all_same(Grid, R, C, Size, Char),
    !,
    Result = Char.
solve(Grid, R, C, Size, Result) :-
    Size > 1,
    Half is Size // 2,
    R1 is R, C1 is C,
    R2 is R, C2 is C + Half,
    R3 is R + Half, C3 is C,
    R4 is R + Half, C4 is C + Half,
    solve(Grid, R1, C1, Half, TL),
    solve(Grid, R2, C2, Half, TR),
    solve(Grid, R3, C3, Half, BL),
    solve(Grid, R4, C4, Half, BR),
    atomic_list_concat(['(', TL, TR, BL, BR, ')'], Result).

main :-
    read_line_to_string(user_input, Line1),
    ( Line1 = end_of_file ->
        true
    ; number_string(N, Line1),
      read_grid(N, Grid),
      solve(Grid, 0, 0, N, Result),
      write(Result), nl
    ).