main :-
    read(M),
    read(N),
    length(Row0, N),
    maplist(=(1), Row0),
    M1 is M - 1,
    iterate(M1, Row0, Row),
    last(Row, Ans),
    writeln(Ans).

iterate(0, Row, Row).
iterate(K, Row, R) :-
    K > 0,
    next_row(Row, NewRow),
    K1 is K - 1,
    iterate(K1, NewRow, R).

next_row([_|Os], [1|Rest]) :-
    cum(Os, 1, Rest).

cum([], _, []).
cum([O|Os], Prev, [Y|Ys]) :-
    Y is Prev + O,
    cum(Os, Y, Ys).

last([X], X).
last([_|T], X) :-
    last(T, X).