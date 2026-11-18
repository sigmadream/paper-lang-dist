main :-
    read_nonempty_line(Line),
    ( Line == end_of_file ->
        true
    ; split_string(Line, " \t\r\n", " \t\r\n", Parts),
      Parts = [NumStr|_],
      number_string(N, NumStr),
      read_rows(N, Grid),
      solve(Grid, 0, 0, N, Ans),
      format("~s~n", [Ans])
    ).

read_nonempty_line(Line) :-
    read_line_to_string(user_input, L),
    ( L == end_of_file ->
        Line = end_of_file
    ; L == "" ->
        read_nonempty_line(Line)
    ; Line = L
    ).

read_rows(0, []) :- !.
read_rows(N, Rows) :-
    N > 0,
    read_nonempty_line(Line),
    N1 is N - 1,
    Rows = [Line|Rest],
    read_rows(N1, Rest).

solve(Grid, R, C, Size, Out) :-
    ( same_region(Grid, R, C, Size, First) ->
        string_codes(Out, [First])
    ; Half is Size // 2,
      R2 is R + Half,
      C2 is C + Half,
      solve(Grid, R, C, Half, TL),
      solve(Grid, R, C2, Half, TR),
      solve(Grid, R2, C, Half, BL),
      solve(Grid, R2, C2, Half, BR),
      string_concat("(", TL, T1),
      string_concat(T1, TR, T2),
      string_concat(T2, BL, T3),
      string_concat(T3, BR, T4),
      string_concat(T4, ")", Out)
    ).

same_region(Grid, R, C, Size, First) :-
    nth0(R, Grid, Row),
    string_code(C, Row, First),
    Size1 is Size - 1,
    \+ ( between(0, Size1, I),
         between(0, Size1, J),
         R2 is R + I,
         C2 is C + J,
         nth0(R2, Grid, Row2),
         string_code(C2, Row2, Code),
         Code =\= First
       ).