main :-
    ( read_line_to_string(user_input, S) ->
        ( S == end_of_file -> true ; solve(S) )
    ; true
    ).

solve(S) :-
    string_chars(S, Cs),
    reverse(Cs, Rs),
    ( Cs == Rs -> writeln(1) ; writeln(0) ).