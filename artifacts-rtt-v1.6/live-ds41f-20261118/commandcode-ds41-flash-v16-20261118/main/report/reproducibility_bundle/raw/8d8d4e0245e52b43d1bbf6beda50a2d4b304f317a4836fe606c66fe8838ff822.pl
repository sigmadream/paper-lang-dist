main :-
    current_input(Stream),
    read_string(Stream, end_of_file, Input),
    split_string(Input, " \t\r\n", " \t\r\n", Tokens),
    parse_numbers(Tokens, Numbers),
    Numbers = [N|Scores],
    solve(N, Scores, Result),
    format("~w~n", [Result]).

token_number(Token, Number) :-
    catch(number_string(Number, Token), _, fail).

parse_numbers([], []).
parse_numbers([Token|Tokens], Numbers) :-
    (   token_number(Token, Number)
    ->  Numbers = [Number|Rest]
    ;   Numbers = Rest
    ),
    parse_numbers(Tokens, Rest).

solve(0, _, 0) :- !.
solve(1, Scores, Result) :-
    !,
    nth0(0, Scores, S1),
    Result = S1.
solve(2, Scores, Result) :-
    !,
    nth0(0, Scores, S1),
    nth0(1, Scores, S2),
    Result is S1 + S2.
solve(N, Scores, Result) :-
    nth0(0, Scores, S1),
    nth0(1, Scores, S2),
    Dp2 is S1 + S2,
    build_dp(3, N, Scores, [0, S1, Dp2], Result).

build_dp(I, N, Scores, DP, Result) :-
    (   I > N
    ->  nth0(N, DP, Result)
    ;   I1 is I - 1,
        nth0(I1, Scores, Si),
        I_minus_2 is I - 2,
        I_minus_3 is I - 3,
        Score_index is I - 2,
        nth0(I_minus_2, DP, Dp_i2),
        nth0(I_minus_3, DP, Dp_i3),
        nth0(Score_index, Scores, S_prev),
        Candidate2 is Dp_i3 + S_prev,
        (   Dp_i2 >= Candidate2
        ->  Best = Dp_i2
        ;   Best = Candidate2
        ),
        Cur is Best + Si,
        append(DP, [Cur], DP2),
        Next is I + 1,
        build_dp(Next, N, Scores, DP2, Result)
    ).