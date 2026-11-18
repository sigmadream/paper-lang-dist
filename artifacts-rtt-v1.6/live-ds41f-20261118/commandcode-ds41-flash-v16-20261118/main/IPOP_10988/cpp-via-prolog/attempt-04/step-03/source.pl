:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  true
    ;   string_codes(S, Cs0),
        delete(Cs0, 0'\r, Cs),
        reverse(Cs, Rs),
        (   Cs == Rs
        ->  writeln(1)
        ;   writeln(0)
        )
    ).