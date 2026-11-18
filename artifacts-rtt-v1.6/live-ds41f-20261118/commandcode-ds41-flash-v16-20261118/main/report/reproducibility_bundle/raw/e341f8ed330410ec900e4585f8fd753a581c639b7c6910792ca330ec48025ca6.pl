main :-
    read_line_to_string(user_input, S),
    ( S == end_of_file ->
        true
    ;
        string_codes(S, Cs),
        reverse(Cs, Rev),
        ( Cs == Rev -> write(1) ; write(0) ),
        nl
    ).