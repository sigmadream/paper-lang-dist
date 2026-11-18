:- module(main, [main/0]).

main :-
    current_input(In),
    read_line_to_codes(In, Line),
    (   Line == end_of_file
    ->  true
    ;   reverse(Line, Rev),
        (   Line == Rev
        ->  write(1)
        ;   write(0)
        ),
        nl
    ).