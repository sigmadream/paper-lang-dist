main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [SM, SN | _],
    number_string(M, SM),
    number_string(N, SN),
    unique_paths(M, N, Ans),
    format('~w~n', [Ans]).

unique_paths(M, N, Ans) :-
    make_ones(N, Row0),
    Rows is M - 1,
    iterate_rows(Rows, Row0, FinalRow),
    list_last(FinalRow, Ans).

make_ones(0, []).
make_ones(N, [1 | T]) :-
    N > 0,
    N1 is N - 1,
    make_ones(N1, T).

iterate_rows(0, Row, Row).
iterate_rows(K, Row, Final) :-
    K > 0,
    update_row(Row, NewRow),
    K1 is K - 1,
    iterate_rows(K1, NewRow, Final).

update_row([First | Rest], NewRow) :-
    update_row_acc(Rest, First, [First], RevNew),
    reverse(RevNew, NewRow).

update_row_acc([], _, Acc, Acc).
update_row_acc([Old | Olds], PrevNew, Acc, New) :-
    Cur is PrevNew + Old,
    update_row_acc(Olds, Cur, [Cur | Acc], New).

list_last([X], X).
list_last([_ | T], X) :-
    list_last(T, X).