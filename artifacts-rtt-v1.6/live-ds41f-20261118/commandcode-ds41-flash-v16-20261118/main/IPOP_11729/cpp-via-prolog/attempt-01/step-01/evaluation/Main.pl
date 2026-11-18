move(1, S, _, E) --> !, [C1, 32, C2, 10], { C1 is 48 + S, C2 is 48 + E }.
move(N, S, M, E) -->
    { N1 is N - 1 },
    move(N1, S, E, M),
    [C1, 32, C2, 10],
    { C1 is 48 + S, C2 is 48 + E },
    move(N1, M, S, E).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", [NStr|_]),
    number_string(N, NStr),
    Count is 2^N - 1,
    format("~w~n", [Count]),
    phrase(move(N, 1, 2, 3), Codes),
    format("~s", [Codes]).