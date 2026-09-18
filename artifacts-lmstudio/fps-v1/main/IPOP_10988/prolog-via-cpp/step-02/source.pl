main :-
    read_line_to_string(Input),
    reverse_string(Input, Reversed),
    (Input = Reversed -> write(1); write(0)),
    nl.

reverse_string(String, Reversed) :-
    string_chars(String, Chars),
    reverse(Chars, Reversed).