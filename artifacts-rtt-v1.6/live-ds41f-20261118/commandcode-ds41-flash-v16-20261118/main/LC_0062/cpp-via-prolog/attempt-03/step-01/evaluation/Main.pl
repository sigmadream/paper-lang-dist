:- use_module(library(readutil)).

read_pair(M, N) :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [A, B | _],
    number_string(M, A),
    number_string(N, B).

next_row([], _, Acc, Row) :-
    reverse(Acc, Row).
next_row([X | Xs], Left, Acc, Row) :-
    Y is X + Left,
    next_row(Xs, Y, [Y | Acc], Row).

next_row(Row, NewRow) :-
    Row = [First | Rest],
    next_row(Rest, First, [First], NewRow).

iterate_rows(0, Row, Row).
iterate_rows(K, Row, Final) :-
    K > 0,
    next_row(Row, NewRow),
    K1 is K - 1,
    iterate_rows(K1, NewRow, Final).

unique_paths(M, N, Ans) :-
    length(Row, N),
    maplist(=(1), Row),
    M1 is M - 1,
    iterate_rows(M1, Row, Final),
    last(Final, Ans).

main :-
    read_pair(M, N),
    unique_paths(M, N, Ans),
    format("~w~n", [Ans]).