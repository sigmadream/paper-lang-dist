main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \n\r\t", " \n\r\t", RawTokens),
    filter_nonempty(RawTokens, Tokens),
    maplist(number_string, Nums, Tokens),
    Nums = [N|Scores],
    solve(N, Scores, Ans),
    format('~w~n', [Ans]).

filter_nonempty([], []).
filter_nonempty([""|T], R) :-
    filter_nonempty(T, R).
filter_nonempty([H|T], [H|R]) :-
    H \= "",
    filter_nonempty(T, R).

solve(1, [A|_], A).
solve(2, [A,B|_], Ans) :-
    Ans is A + B.
solve(N, [A,B|Rest], Ans) :-
    N >= 3,
    Dp2Init is A + B,
    loop(Rest, 0, A, Dp2Init, B, Ans).

loop([], _, _, Dp2, _, Dp2).
loop([X|Xs], Dp0, Dp1, Dp2, Prev, Ans) :-
    Best is max(Dp1, Dp0 + Prev),
    Dp is Best + X,
    loop(Xs, Dp1, Dp2, Dp, X, Ans).