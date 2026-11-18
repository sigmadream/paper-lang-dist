main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   split_string(Codes, " \t", " \t", [MStr, NStr]),
        number_codes(M, MStr),
        number_codes(N, NStr),
        unique_paths(M, N, Ans),
        format("~w~n", [Ans])
    ).

unique_paths(M, N, Ans) :-
    length(Row, N),
    maplist(=(1), Row),
    Rows is M - 1,
    iterate_rows(Rows, Row, Final),
    last(Final, Ans).

iterate_rows(0, Row, Row) :- !.
iterate_rows(K, Row, Final) :-
    update_row(Row, NewRow),
    K1 is K - 1,
    iterate_rows(K1, NewRow, Final).

update_row([X|Xs], [X|Ys]) :-
    update_tail(Xs, X, Ys).

update_tail([], _, []).
update_tail([C|Cs], Prev, [New|Rest]) :-
    New is Prev + C,
    update_tail(Cs, New, Rest).