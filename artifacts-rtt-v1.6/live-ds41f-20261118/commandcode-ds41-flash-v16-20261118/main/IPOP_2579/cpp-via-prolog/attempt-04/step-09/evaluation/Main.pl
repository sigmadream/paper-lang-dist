:- use_module(library(readutil)).

main :-
    read_all_tokens(Tokens),
    (   Tokens = []
    ->  true
    ;   Tokens = [NStr|ScoreStrList],
        number_string(N, NStr),
        length(ScoreStrs, N),
        append(ScoreStrs, _, ScoreStrList),
        maplist(token_number, ScoreStrs, Scores),
        solve(N, Scores, Answer),
        format("~w~n", [Answer])
    ).

read_all_tokens(Tokens) :-
    read_lines(Lines),
    maplist(split_line_tokens, Lines, TokenLists),
    append(TokenLists, Tokens).

read_lines(Lines) :-
    read_line_to_string(current_input, Line),
    (   Line == end_of_file
    ->  Lines = []
    ;   Lines = [Line|Rest],
        read_lines(Rest)
    ).

split_line_tokens(Line, Tokens) :-
    split_string(Line, " \t\r", " \t\r", Tokens).

token_number(Str, Num) :-
    number_string(Num, Str).

solve(1, [S1], S1).
solve(2, [S1, S2], Answer) :-
    Answer is S1 + S2.
solve(N, [S1, S2|Rest], Answer) :-
    N >= 3,
    Dp0 = 0,
    Dp1 = S1,
    Dp2 is S1 + S2,
    compute_from(3, N, Rest, S2, Dp0, Dp1, Dp2, Answer).

compute_from(I, N, Rest, PreviousScore, Dp0, Dp1, Dp2, Answer) :-
    (   I > N
    ->  Answer = Dp2
    ;   Rest = [Si|Rest1],
        Option1 is Dp1 + Si,
        Option2 is Dp0 + PreviousScore + Si,
        DpI is max(Option1, Option2),
        I1 is I + 1,
        compute_from(I1, N, Rest1, Si, Dp1, Dp2, DpI, Answer)
    ).