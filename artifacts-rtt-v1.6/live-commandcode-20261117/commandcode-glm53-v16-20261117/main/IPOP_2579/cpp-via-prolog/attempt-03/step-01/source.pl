:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

main :-
    read_line_to_codes(user_input, L1),
    parse_int(L1, N),
    read_scores(N, Scores0),
    reverse(Scores0, Scores), % Scores: stair 1..N in order
    length(Scores, N),
    solve(N, Scores, Ans),
    format("~d~n", [Ans]).

read_scores(0, []) :- !.
read_scores(N, [S|Rest]) :-
    read_line_to_codes(user_input, L),
    parse_int(L, S),
    N1 is N - 1,
    read_scores(N1, Rest).

parse_int(L, X) :-
    number_codes(X, L).

solve(N, Scores, Ans) :-
    length(Dp, N),
    fill_dp(N, Scores, Dp),
    nth1(N, Dp, Ans).

fill_dp(1, [S1], [S1]) :- !.
fill_dp(2, [S1, S2], [D1, D2]) :- !,
    D1 is S1,
    D2 is S1 + S2.
fill_dp(N, Scores, Dp) :-
    N >= 3,
    Nm1 is N - 1,
    Nm2 is N - 2,
    Nm3 is N - 3,
    fill_dp(Nm1, Scores, Dp1),
    nth1(Nm1, Dp1, Dm1),
    nth1(Nm2, Dp1, Dm2),
    nth1(Nm3, Dp1, Dm3),
    nth1(N, Scores, SN),
    nth1(Nm1, Scores, SNm1),
    D is max(Dm2, Dm3 + SNm1) + SN,
    append(Dp1, [D], Dp).