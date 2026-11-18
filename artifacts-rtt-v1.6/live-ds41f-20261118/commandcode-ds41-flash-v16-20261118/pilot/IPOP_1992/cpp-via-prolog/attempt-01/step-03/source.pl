main :-
    read_line_to_string(user_input, NLine),
    number_string(N, NLine),
    read_grid(N, Grid),
    solve(0, 0, N, Grid, Answer),
    write(Answer),
    nl.

read_grid(0, []) :- !.
read_grid(N, [Row|Rest]) :-
    read_line_to_string(user_input, Line),
    string_chars(Line, Row),
    N1 is N - 1,
    read_grid(N1, Rest).

get_cell(R, C, Grid, V) :-
    nth0(R, Grid, Row),
    nth0(C, Row, V).

all_same(R, C, S, V, Grid) :-
    EndR is R + S - 1,
    EndC is C + S - 1,
    all_rows(R, EndR, C, EndC, V, Grid).

all_rows(I, EndR, _, _, _, _) :-
    I > EndR, !.
all_rows(I, EndR, C, EndC, V, Grid) :-
    nth0(I, Grid, Row),
    all_cols(C, EndC, Row, V),
    I1 is I + 1,
    all_rows(I1, EndR, C, EndC, V, Grid).

all_cols(J, EndC, _, _) :-
    J > EndC, !.
all_cols(J, EndC, Row, V) :-
    nth0(J, Row, V),
    J1 is J + 1,
    all_cols(J1, EndC, Row, V).

solve(R, C, S, Grid, Out) :-
    get_cell(R, C, Grid, V),
    (   all_same(R, C, S, V, Grid)
    ->  Out = V
    ;   Half is S // 2,
        R2 is R + Half,
        C2 is C + Half,
        solve(R, C, Half, Grid, O1),
        solve(R, C2, Half, Grid, O2),
        solve(R2, C, Half, Grid, O3),
        solve(R2, C2, Half, Grid, O4),
        atomic_list_concat(['(', O1, O2, O3, O4, ')'], Out)
    ).