:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    Parts = [MStr, NStr | _],
    number_string(M, MStr),
    number_string(N, NStr),
    length(DP0, N),
    maplist(=(1), DP0),
    Rows is M - 1,
    iterate_rows(Rows, DP0, DP),
    last(DP, Answer),
    writeln(Answer).

iterate_rows(0, DP, DP) :- !.
iterate_rows(K, DP, Result) :-
    K > 0,
    update_dp(DP, DP1),
    K1 is K - 1,
    iterate_rows(K1, DP1, Result).

update_dp([X | Xs], [X | Ys]) :-
    update_dp_helper(Xs, X, Ys).

update_dp_helper([], _, []).
update_dp_helper([A | As], Prev, [B | Bs]) :-
    B is A + Prev,
    update_dp_helper(As, B, Bs).