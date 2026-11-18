main :-
    read_string(user_input, end_of_file, Input),
    string_codes(Input, Codes),
    parse_ints(Codes, Nums),
    ( Nums = [N|Scores] ->
        take_n(N, Scores, Used),
        solve(N, Used, Answer),
        write(Answer), nl
    ; true
    ).

take_n(0, _, []).
take_n(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, Xs, Ys).

solve(1, [S], S) :- !.
solve(2, [S0,S1], A) :- !,
    A is S0 + S1.
solve(N, [S0,S1|Rest], Answer) :-
    N >= 3,
    D1 is S0 + S1,
    dp(Rest, 0, S0, D1, S1, Answer).

dp([], _, _, D1, _, D1).
dp([Cur|Tail], D3, D2, D1, Prev, Answer) :-
    X is D3 + Prev,
    ( D2 >= X -> Best = D2 ; Best = X ),
    Di is Best + Cur,
    dp(Tail, D2, D1, Di, Cur, Answer).

parse_ints([], []).
parse_ints(Codes, Nums) :-
    skip_ws(Codes, Rest),
    ( Rest = [] ->
        Nums = []
    ; parse_one_int(Rest, Num, Rest1),
      Nums = [Num|Tail],
      parse_ints(Rest1, Tail)
    ).

skip_ws([C|Cs], Rest) :-
    is_ws(C), !,
    skip_ws(Cs, Rest).
skip_ws(Rest, Rest).

is_ws(32).
is_ws(9).
is_ws(10).
is_ws(13).

parse_one_int([C|Cs], Num, Rest) :-
    C >= 48, C =< 57, !,
    parse_digits(Cs, C, Num, Rest).

parse_digits([C|Cs], Acc, Num, Rest) :-
    C >= 48, C =< 57, !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(Cs, Acc1, Num, Rest).
parse_digits(Rest, Num, Num, Rest).