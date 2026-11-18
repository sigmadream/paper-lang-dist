:- use_module(library(readutil)).

main :-
    read_all_codes(Codes),
    parse_int_tokens(Codes, Tokens),
    Tokens = [N|Scores],
    take_n(N, Scores, ScoreList),
    solve(N, ScoreList, Answer),
    writeln(Answer).

read_all_codes(Codes) :-
    read_line_to_codes(user_input, Line),
    (   Line == end_of_file
    ->  Codes = []
    ;   read_all_codes(Rest),
        append(Line, [32|Rest], Codes)
    ).

parse_int_tokens(Codes, Ints) :-
    skip_ws(Codes, Rest),
    (   Rest == []
    ->  Ints = []
    ;   parse_number(Rest, Num, Rest1),
        Ints = [Num|Tail],
        parse_int_tokens(Rest1, Tail)
    ).

skip_ws([C|Cs], Rest) :-
    C =< 32,
    !,
    skip_ws(Cs, Rest).
skip_ws(Codes, Codes).

parse_number(Codes, Num, Rest) :-
    parse_number_acc(Codes, 0, Num, Rest).

parse_number_acc([C|Cs], Acc, Num, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_number_acc(Cs, Acc1, Num, Rest).
parse_number_acc(Rest, Acc, Acc, Rest).

take_n(0, _, []) :- !.
take_n(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, Xs, Ys).

solve(1, [S1|_], S1).
solve(2, [S1,S2|_], Answer) :-
    Answer is S1 + S2.
solve(N, [S1,S2|Rest], Answer) :-
    N >= 3,
    Dp1 is S1,
    Dp2 is S1 + S2,
    compute_rest(Rest, S2, 0, Dp1, Dp2, Answer).

compute_rest([], _, _, _, DpLast, DpLast).
compute_rest([S|Ss], PrevS, DpIM3, DpIM2, DpIM1, Answer) :-
    TakeTwo is DpIM2 + S,
    TakeOne is DpIM3 + PrevS + S,
    Dp is max(TakeTwo, TakeOne),
    compute_rest(Ss, S, DpIM2, DpIM1, Dp, Answer).