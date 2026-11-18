:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

main :-
    current_input(In),
    read_line_to_codes(In, Line),
    (   Line == end_of_file -> true
    ;   reverse(Line, Rev),
        (   Line == Rev -> N = "1"
        ;   N = "0"
        ),
        format("~s~n", [N])
    ).