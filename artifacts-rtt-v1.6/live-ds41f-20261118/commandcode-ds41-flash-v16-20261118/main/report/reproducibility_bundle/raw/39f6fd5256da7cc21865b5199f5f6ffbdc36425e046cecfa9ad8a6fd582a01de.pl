main :-
    ( read_line_to_string(user_input, Line) ->
        ( Line == end_of_file ->
            true
        ; string_codes(Line, Codes0),
          strip_newline(Codes0, Codes),
          string_codes(S, Codes),
          ( palindrome(S) -> writeln(1) ; writeln(0) )
        )
    ; true
    ).

strip_newline([], []).
strip_newline([C|Cs], Rest) :-
    ( C =:= 10 ; C =:= 13 ),
    !,
    strip_newline(Cs, Rest).
strip_newline([C|Cs], [C|Rest]) :-
    strip_newline(Cs, Rest).

palindrome(S) :-
    string_codes(S, Cs),
    reverse(Cs, Cs).