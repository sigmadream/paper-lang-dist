:- use_module(library(readutil)).

main :-
    read_tokens(Tokens),
    Tokens = [NStr|Rest],
    number_string(N, NStr),
    take(N, Rest, ScoreStrList),
    maplist(number_string, Scores, ScoreStrList),
    solve(Scores, Answer),
    writeln(Answer).

read_tokens(Tokens) :-
    read_tokens_rev([], Rev),
    reverse(Rev, Tokens).

read_tokens_rev(Acc, Rev) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Rev = Acc
    ; split_string(Line, " \t\r\n", " \t\r\n", Ts),
      reverse(Ts, RevTs),
      append(RevTs, Acc, Acc2),
      read_tokens_rev(Acc2, Rev)
    ).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

solve(Scores, Answer) :-
    length(Scores, N),
    ( N =:= 1 ->
        nth1(1, Scores, Answer)
    ; N =:= 2 ->
        nth1(1, Scores, S1),
        nth1(2, Scores, S2),
        Answer is S1 + S2
    ; nth1(1, Scores, S1),
      nth1(2, Scores, S2),
      DP2 is S1 + S2,
      DP = [S1, DP2],
      compute(3, N, Scores, DP, Answer)
    ).

compute(I, N, _, DP, Answer) :-
    I > N,
    !,
    reverse(DP, [Answer|_]).
compute(I, N, Scores, DP, Answer) :-
    nth1(I, Scores, Si),
    SPrevIdx is I - 1,
    nth1(SPrevIdx, Scores, SPrev),
    ( I =:= 3 ->
        nth1(1, DP, DP1),
        max_num(DP1, SPrev, Candidate)
    ; Idx2 is I - 2,
      Idx3 is I - 3,
      nth1(Idx2, DP, DP_i2),
      nth1(Idx3, DP, DP_i3),
      Tmp is DP_i3 + SPrev,
      max_num(DP_i2, Tmp, Candidate)
    ),
    NewDP is Candidate + Si,
    append(DP, [NewDP], DP2),
    I1 is I + 1,
    compute(I1, N, Scores, DP2, Answer).

max_num(A, B, M) :-
    ( A >= B -> M = A ; M = B ).