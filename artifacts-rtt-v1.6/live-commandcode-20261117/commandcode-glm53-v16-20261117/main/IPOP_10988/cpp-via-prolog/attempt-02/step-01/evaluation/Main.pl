:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, string).

main :-
    read_line_to_string(user_input, S),
    (   S == end_of_file ->
        true
    ;   string_length(S, Len),
        (   palindrome(S, Len) ->
            writeln(1)
        ;   writeln(0)
        )
    ).

palindrome(S, Len) :-
    Half is Len // 2,
    check(S, 0, Half, Len).

check(_, I, Half, _) :-
    I >= Half, !.
check(S, I, Half, Len) :-
    J is Len - 1 - I,
    string_code(I, S, C1),
    string_code(J, S, C2),
    C1 == C2,
    I1 is I + 1,
    check(S, I1, Half, Len).