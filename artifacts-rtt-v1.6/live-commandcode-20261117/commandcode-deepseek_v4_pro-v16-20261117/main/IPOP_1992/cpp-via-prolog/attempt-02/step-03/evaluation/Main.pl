main :-
    read_input(N, Grid),
    solve(Grid, 0, 0, N, Result),
    atomic_list_concat(Result, '', Output),
    write(Output), nl.

read_input(N, Grid) :-
    read_line_to_string(user_input, Line1),
    Line1 \= end_of_file,
    number_string(N, Line1),
    read_lines(N, Grid).

read_lines(0, []) :- !.
read_lines(N, [Line|Rest]) :-
    N > 0,
    read_line_to_string(user_input, Line),
    Line \= end_of_file,
    N1 is N - 1,
    read_lines(N1, Rest).

solve(Grid, R, C, 1, [Char]) :-
    nth0(R, Grid, Row), nth0(C, Row, Char), !.
solve(Grid, R, C, Size, Result) :-
    Size > 1,
    nth0(R, Grid, Row0), nth0(C, Row0, First),
    (   check_all(Grid, R, C, Size, First)
    ->  Result = [First]
    ;   Half is Size // 2,
        solve(Grid, R, C, Half, TL),
        solve(Grid, R, C + Half, Half, TR),
        solve(Grid, R + Half, C, Half, BL),
        solve(Grid, R + Half, C + Half, Half, BR),
        append([['('], TL, TR, BL, BR, [')']], Result)
    ).

check_all(Grid, R, C, Size, First) :-
    findall(Char,
            (   between(0, Size-1, DR),
                between(0, Size-1, DC),
                RR is R + DR,
                CC is C + DC,
                nth0(RR, Grid, Row),
                nth0(CC, Row, Char)
            ),
            Chars),
    maplist(==(First), Chars).