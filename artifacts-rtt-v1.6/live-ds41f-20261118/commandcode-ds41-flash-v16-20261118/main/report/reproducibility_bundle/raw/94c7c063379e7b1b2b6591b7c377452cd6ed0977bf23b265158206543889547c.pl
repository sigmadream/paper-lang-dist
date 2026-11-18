:- use_module(library(readline)).

main :-
    read_line_to_string(user_input, Line0),
    Line0 \== end_of_file,
    clean_line(Line0, Line),
    number_string(N, Line),
    read_grid(N, Grid),
    solve(Grid, 0, 0, N, Result),
    string_chars(Out, Result),
    format("~s~n", [Out]).

clean_line(Line, Clean) :-
    string_codes(Line, Codes0),
    remove_cr(Codes0, Codes),
    string_codes(Clean, Codes).

remove_cr([], []).
remove_cr([0'\r|T], R) :-
    !,
    remove_cr(T, R).
remove_cr([H|T], [H|R]) :-
    remove_cr(T, R).

read_grid(0, []) :-
    !.
read_grid(N, [Chars|Rest]) :-
    N > 0,
    read_line_to_string(user_input, Line0),
    clean_line(Line0, Line),
    string_chars(Line, Chars),
    N1 is N - 1,
    read_grid(N1, Rest).

solve(Grid, R, C, S, Result) :-
    nth0(R, Grid, Row),
    nth0(C, Row, First),
    (   same_region(Grid, R, C, S, First)
    ->  Result = [First]
    ;   H is S // 2,
        R2 is R + H,
        C2 is C + H,
        solve(Grid, R, C, H, TL),
        solve(Grid, R, C2, H, TR),
        solve(Grid, R2, C, H, BL),
        solve(Grid, R2, C2, H, BR),
        append(TL, TR, A),
        append(A, BL, B),
        append(B, BR, Body),
        Result = ['('|Rest],
        append(Body, [')'], Rest)
    ).

same_region(Grid, R, C, S, Val) :-
    EndR is R + S,
    EndC is C + S,
    same_rows(Grid, R, EndR, C, EndC, Val).

same_rows(_, R, EndR, _, _, _) :-
    R >= EndR,
    !.
same_rows(Grid, R, EndR, C, EndC, Val) :-
    nth0(R, Grid, Row),
    same_cols(Row, C, EndC, Val),
    R1 is R + 1,
    same_rows(Grid, R1, EndR, C, EndC, Val).

same_cols(_, C, EndC, _) :-
    C >= EndC,
    !.
same_cols(Row, C, EndC, Val) :-
    nth0(C, Row, Val),
    C1 is C + 1,
    same_cols(Row, C1, EndC, Val).