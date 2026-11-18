:- use_module(library(readutil)).

main :-
    current_input(In),
    read_line_to_codes(In, Line1),
    ( Line1 == end_of_file ->
        true
    ;
        split_line(Line1, NStr),
        number_codes(N, NStr),
        read_rows(In, N, Rows),
        solve(Rows, 0, 0, N, Out),
        append(Out, Flat),
        format("~s~n", [Flat])
    ).

split_line(L, L2) :-
    ( append(L2, [10], L) -> true ; L2 = L ).

read_rows(_, 0, []) :- !.
read_rows(In, N, [Row|Rest]) :-
    read_line_to_codes(In, L),
    ( L == end_of_file ->
        Rest = [],
        N1 = 0
    ;
        ( L == [] ->
            read_rows(In, N, [Row|Rest])
        ;
            split_line(L, Row),
            N1 is N - 1,
            read_rows(In, N1, Rest)
        )
    ).

cell(Grid, R, C, X) :-
    nth0(R, Grid, Row),
    nth0(C, Row, X).

uniform(Grid, R, C, S, X) :-
    cell(Grid, R, C, X),
    EndR is R + S,
    EndC is C + S,
    forall(between(R, EndR1, EndR),
           ( EndR1 is EndR - 1,
             between(C, EndC1, EndC),
             EndC1 is EndC - 1,
             cell(Grid, EndR1, EndC1, X)
           )).

solve(Grid, R, C, S, Out) :-
    ( uniform(Grid, R, C, S, X) ->
        Out = [X]
    ;
        H is S // 2,
        RH is R + H,
        CH is C + H,
        solve(Grid, R, C, H, TL),
        solve(Grid, R, CH, H, TR),
        solve(Grid, RH, C, H, BL),
        solve(Grid, RH, CH, H, BR),
        Out = [[0'(], TL, TR, BL, BR, [0'))]]
    ).