parse_int_line(Line, N) :-
    split_string(Line, " \t\r", " \t\r", [Token|_]),
    number_string(N, Token).

read_scores(0, []) :- !.
read_scores(N, [S|Ss]) :-
    read_line_to_string(user_input, Line),
    parse_int_line(Line, S),
    N1 is N - 1,
    read_scores(N1, Ss).

max_val(A, B, A) :- A >= B, !.
max_val(_, B, B).

dp_value(1, Scores, _, Val) :-
    nth1(2, Scores, Val).
dp_value(2, Scores, _, Val) :-
    nth1(2, Scores, S1),
    nth1(3, Scores, S2),
    Val is S1 + S2.
dp_value(I, Scores, DpIn, Val) :-
    I >= 3,
    Idx2 is I - 1,
    Idx3 is I - 2,
    nth1(Idx2, DpIn, DP2),
    nth1(Idx3, DpIn, DP3),
    nth1(I, Scores, SPrev),
    IdxCur is I + 1,
    nth1(IdxCur, Scores, SCur),
    PrevBest is DP3 + SPrev,
    max_val(DP2, PrevBest, Best),
    Val is Best + SCur.

build_dp(I, N, _, Dp, Dp) :- I > N, !.
build_dp(I, N, Scores, DpIn, DpOut) :-
    dp_value(I, Scores, DpIn, Val),
    append(DpIn, [Val], DpNext),
    I1 is I + 1,
    build_dp(I1, N, Scores, DpNext, DpOut).

solve(N, Scores, Result) :-
    Scores1 = [0|Scores],
    build_dp(1, N, Scores1, [0], Dp),
    Idx is N + 1,
    nth1(Idx, Dp, Result).

main :-
    read_line_to_string(user_input, NLine),
    parse_int_line(NLine, N),
    read_scores(N, Scores),
    solve(N, Scores, Result),
    format("~w~n", [Result]).