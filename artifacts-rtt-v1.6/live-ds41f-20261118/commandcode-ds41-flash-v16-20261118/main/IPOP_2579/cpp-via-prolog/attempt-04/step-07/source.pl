main :-
    read_all_lines([], RevLines),
    reverse(RevLines, Lines),
    tokenize_lines(Lines, Tokens),
    (   Tokens = [NToken|RestTokens]
    ->  number_codes(N, NToken),
        take_tokens(N, RestTokens, ScoreTokens),
        parse_scores(ScoreTokens, Scores),
        solve(N, Scores, Ans),
        write(Ans), nl
    ;   true
    ).

read_all_lines(Acc, Lines) :-
    read_line_to_codes(user_input, Line),
    (   Line == end_of_file
    ->  Lines = Acc
    ;   read_all_lines([Line|Acc], Lines)
    ).

tokenize_lines([], []).
tokenize_lines([Line|Lines], Tokens) :-
    split_ws(Line, T1),
    tokenize_lines(Lines, T2),
    append(T1, T2, Tokens).

split_ws([], []).
split_ws([C|Cs], Tokens) :-
    (   C =< 32
    ->  split_ws(Cs, Tokens)
    ;   take_token(Cs, [C], Rest, Token),
        Tokens = [Token|Tokens1],
        split_ws(Rest, Tokens1)
    ).

take_token([], Acc, [], Token) :-
    reverse(Acc, Token).
take_token([C|Cs], Acc, Rest, Token) :-
    (   C =< 32
    ->  reverse(Acc, Token),
        Rest = Cs
    ;   take_token(Cs, [C|Acc], Rest, Token)
    ).

take_tokens(0, _, []) :- !.
take_tokens(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take_tokens(N1, Xs, Ys).

parse_scores([], []).
parse_scores([T|Ts], [S|Ss]) :-
    number_codes(S, T),
    parse_scores(Ts, Ss).

solve(1, [S1|_], Ans) :-
    Ans is S1.
solve(2, [S1,S2|_], Ans) :-
    Ans is S1 + S2.
solve(N, [S1,S2,S3|Rest], Ans) :-
    N >= 3,
    Dp0 = 0,
    Dp1 is S1,
    Dp2 is S1 + S2,
    compute_dp(3, N, S2, [S3|Rest], Dp0, Dp1, Dp2, Ans).

compute_dp(I, N, PrevScore, Scores, Dp_im3, Dp_im2, Dp_im1, Ans) :-
    (   I > N
    ->  Ans = Dp_im1
    ;   Scores = [CurScore|RestScores],
        Option1 is Dp_im2 + CurScore,
        Option2 is Dp_im3 + PrevScore + CurScore,
        (   Option1 >= Option2
        ->  DpI = Option1
        ;   DpI = Option2
        ),
        I1 is I + 1,
        compute_dp(I1, N, CurScore, RestScores, Dp_im2, Dp_im1, DpI, Ans)
    ).