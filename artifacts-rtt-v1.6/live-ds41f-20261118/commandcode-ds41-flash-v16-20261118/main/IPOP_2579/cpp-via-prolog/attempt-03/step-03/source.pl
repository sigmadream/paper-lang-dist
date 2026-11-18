:- use_module(library(readutil)).

main :-
    read_lines(Lines),
    collect_numbers(Lines, Nums),
    Nums = [N|Scores],
    solve(N, Scores, Ans),
    write(Ans), nl.

read_lines(Lines) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  Lines = []
    ;   Lines = [Line|Rest],
        read_lines(Rest)
    ).

collect_numbers([], []).
collect_numbers([Line|Lines], Nums) :-
    line_numbers(Line, LineNums),
    append(LineNums, RestNums, Nums),
    collect_numbers(Lines, RestNums).

line_numbers(Line, Nums) :-
    split_string(Line, " \t\r", " \t\r", Tokens),
    numbers_from_tokens(Tokens, Nums).

numbers_from_tokens([], []).
numbers_from_tokens([Token|Tokens], Nums) :-
    (   catch(number_string(N, Token), _, fail)
    ->  Nums = [N|Rest],
        numbers_from_tokens(Tokens, Rest)
    ;   numbers_from_tokens(Tokens, Nums)
    ).

solve(1, Scores, Ans) :-
    Scores = [S1],
    Ans = S1.
solve(2, Scores, Ans) :-
    Scores = [S1, S2],
    Ans is S1 + S2.
solve(N, Scores, Ans) :-
    N >= 3,
    Scores = [S1, S2, S3|Rest],
    Dp0 = 0,
    Dp1 = S1,
    Dp2 is S1 + S2,
    dp_loop([S3|Rest], Dp0, Dp1, Dp2, S2, Ans).

dp_loop([S|Rest], Dp0, Dp1, Dp2, PrevScore, Ans) :-
    (   Dp1 >= Dp0 + PrevScore
    ->  Best = Dp1
    ;   Best = Dp0 + PrevScore
    ),
    Dp is Best + S,
    (   Rest == []
    ->  Ans = Dp
    ;   dp_loop(Rest, Dp1, Dp2, Dp, S, Ans)
    ).