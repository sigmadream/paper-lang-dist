main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    Parts = [MStr, NStr],
    number_string(M, MStr),
    number_string(N, NStr),
    compute(M, N, Ans),
    format("~w~n", [Ans]).

compute(M, N, Ans) :-
    fill_ones(N, Dp0),
    Steps is M - 1,
    iterate(Steps, Dp0, Dp),
    last(Dp, Ans).

fill_ones(0, []).
fill_ones(N, [1|T]) :-
    N > 0,
    N1 is N - 1,
    fill_ones(N1, T).

iterate(0, Dp, Dp) :- !.
iterate(K, Dp0, Dp) :-
    K > 0,
    update(Dp0, Dp1),
    K1 is K - 1,
    iterate(K1, Dp1, Dp).

update([First|Rest], [First|NewRest]) :-
    update_rest(Rest, First, NewRest).

update_rest([], _, []).
update_rest([X|Xs], Prev, [Y|Ys]) :-
    Y is X + Prev,
    update_rest(Xs, Y, Ys).