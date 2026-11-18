main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    maplist(number_string, [M, N], Parts),
    length(DP, N),
    maplist(=(1), DP),
    Rows is M - 1,
    iterate_rows(Rows, DP, FinalDP),
    last(FinalDP, Answer),
    format("~w~n", [Answer]).

iterate_rows(0, DP, DP) :- !.
iterate_rows(K, DP, FinalDP) :-
    update_dp(DP, NextDP),
    K1 is K - 1,
    iterate_rows(K1, NextDP, FinalDP).

update_dp([First|Rest], [First|NextRest]) :-
    update_rest(Rest, First, NextRest).

update_rest([], _, []).
update_rest([X|Xs], Prev, [Y|Ys]) :-
    Y is X + Prev,
    update_rest(Xs, Y, Ys).