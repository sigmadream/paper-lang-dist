:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line0),
    ( Line0 = end_of_file -> halt ; true ),
    number_string(T, Line0),
    process(T).

process(0) :- !.
process(N) :-
    N > 0,
    read_line_to_string(user_input, S),
    ( S = end_of_file -> halt ; true ),
    ( is_valid(S) -> write('YES'), nl ; write('NO'), nl ),
    N1 is N - 1,
    process(N1).

is_valid(S) :-
    string_chars(S, Chars),
    is_valid_chars(Chars, 0).

is_valid_chars([], Bal) :- Bal =:= 0.
is_valid_chars([C|Cs], Bal) :-
    ( C = '(' ->
        Bal1 is Bal + 1
    ;
        Bal1 is Bal - 1
    ),
    Bal1 >= 0,
    is_valid_chars(Cs, Bal1).