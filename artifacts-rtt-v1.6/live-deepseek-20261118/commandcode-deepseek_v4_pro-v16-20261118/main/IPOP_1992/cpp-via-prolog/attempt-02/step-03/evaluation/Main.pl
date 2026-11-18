main :-
    (   read_line_to_codes(user_input, Line0),
        Line0 \= end_of_file
    ->  number_codes(N, Line0),
        read_n_lines(N, user_input, Grid),
        solve(0, 0, N, Grid, Codes),
        atom_codes(Ans, Codes),
        writeln(Ans)
    ;   true
    ).

read_n_lines(0, _, []) :- !.
read_n_lines(N, Stream, [Line|Lines]) :-
    N > 0,
    read_line_to_codes(Stream, Line),
    Line \= end_of_file,
    N1 is N - 1,
    read_n_lines(N1, Stream, Lines).

cell(Row, Col, Grid, Char) :-
    nth0(Row, Grid, RowList),
    nth0(Col, RowList, Char).

all_same(R, C, Size, Grid, First) :-
    EndR is R + Size - 1,
    EndC is C + Size - 1,
    forall(
        ( between(R, EndR, I),
          between(C, EndC, J) ),
        cell(I, J, Grid, First)
    ).

solve(R, C, Size, Grid, Result) :-
    cell(R, C, Grid, First),
    all_same(R, C, Size, Grid, First),
    !,
    Result = [First].
solve(R, C, Size, Grid, Result) :-
    Half is Size // 2,
    R1 is R + Half,
    C1 is C + Half,
    solve(R, C, Half, Grid, TL),
    solve(R, C1, Half, Grid, TR),
    solve(R1, C, Half, Grid, BL),
    solve(R1, C1, Half, Grid, BR),
    append([TL, TR, BL, BR], Tmp),
    Result = [0'( | Tmp],
    append(Result, [0')], Result2),
    Result = Result2.