:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, chars).

main :-
    read_line_to_string(current_input, S),
    (   S == end_of_file -> true
    ;   string_chars(S, Cs),
        (   palindrome(Cs) -> R = 1 ; R = 0 ),
        format("~d~n", [R])
    ).

palindrome(Cs) :-
    reverse(Cs, Cs).