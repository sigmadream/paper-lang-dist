main :-
    read_line_to_string(Input),
    reverse_string(Input, Reversed),
    (Input == Reversed -> write(1); write(0)),
    nl.

reverse_string(String, Reversed) :-
    reverse_chars(String, [], Reversed).

reverse_chars([], Acc, Acc).
reverse_chars([H|T], Acc, Reversed) :-
    reverse_chars(T, [H|Acc], Reversed).