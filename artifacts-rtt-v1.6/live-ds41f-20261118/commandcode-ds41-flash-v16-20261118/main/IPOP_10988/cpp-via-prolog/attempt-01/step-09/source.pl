main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   string_codes(Line, Codes),
        reverse(Codes, Reversed),
        (   Codes == Reversed
        ->  Result = 1
        ;   Result = 0
        ),
        format("~w~n", [Result])
    ).