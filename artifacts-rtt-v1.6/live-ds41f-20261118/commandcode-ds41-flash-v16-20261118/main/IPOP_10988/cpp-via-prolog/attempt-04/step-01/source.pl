main :-
    read_line_to_codes(user_input, Codes0),
    (   Codes0 == end_of_file
    ->  true
    ;   delete(Codes0, 0'\r, Codes),
        (   reverse(Codes, Codes)
        ->  Result = 1
        ;   Result = 0
        ),
        writeln(Result)
    ).