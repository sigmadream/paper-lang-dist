:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file ->
        true
    ;   parse_t(Line, T) ->
        process(T)
    ;   true
    ).

parse_t(Line, T) :-
    split_string(Line, " \t\r\n", " \t\r\n", [S]),
    number_string(T, S).

process(0).
process(N) :-
    N > 0,
    read_line_to_string(user_input, S),
    (   S == end_of_file ->
        true
    ;   check(S),
        N1 is N - 1,
        process(N1)
    ).

check(S) :-
    (   valid(S) ->
        write('YES')
    ;   write('NO')
    ),
    nl.

valid(S) :-
    split_string(S, " \t\r\n", " \t\r\n", [Clean]),
    string_chars(Clean, Chars),
    valid_chars(Chars, 0).

valid_chars([], 0).
valid_chars(['('|Rest], Bal) :-
    Bal1 is Bal + 1,
    valid_chars(Rest, Bal1).
valid_chars([')'|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    valid_chars(Rest, Bal1).