main :-
    current_input(Stream),
    read_string(Stream, end_of_file, String),
    split_string(String, " \t\n\r", " \t\n\r", Tokens),
    ( Tokens = [] ->
        Ans = 0
    ;
        maplist(number_string, Numbers, Tokens),
        Numbers = [N|Rest0],
        ( Rest0 = [M|Rest] -> true ; M = 0, Rest = [] ),
        take_edges(M, Rest, Edges),
        solve(N, M, Edges, Ans)
    ),
    write(Ans), nl.

take_edges(0, _, []) :- !.
take_edges(M, [A,B|T], [A-B|Es]) :-
    M > 0,
    M1 is M - 1,
    take_edges(M1, T, Es).
take_edges(_, _, []).

solve(_, _, Edges, Ans) :-
    findall(X,
            ( member(A-B, Edges),
              ( A =:= 1 -> X = B
              ; B =:= 1 -> X = A
              ; fail
              )
            ),
            Direct0),
    list_to_set(Direct0, Direct),
    findall(Y,
            ( member(V, Direct),
              member(A-B, Edges),
              ( A =:= V -> Y = B
              ; B =:= V -> Y = A
              ; fail
              ),
              Y =\= 1
            ),
            Second0),
    append(Direct, Second0, All0),
    list_to_set(All0, All),
    length(All, L),
    ( memberchk(1, All) -> Ans is L - 1 ; Ans = L ).