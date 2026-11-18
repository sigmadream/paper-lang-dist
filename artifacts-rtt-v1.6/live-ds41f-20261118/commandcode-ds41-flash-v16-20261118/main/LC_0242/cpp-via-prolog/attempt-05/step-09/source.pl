:- use_module(library(readutil)).

read_line(Line) :-
    read_line_to_string(user_input, X),
    ( X == end_of_file -> Line = "" ; Line = X ).

remove_cr([], []).
remove_cr([13|T], R) :-
    remove_cr(T, R).
remove_cr([C|T], [C|R]) :-
    C \= 13,
    remove_cr(T, R).

sorted_chars(String, Sorted) :-
    string_codes(String, Codes),
    remove_cr(Codes, Clean),
    msort(Clean, Sorted).

main :-
    read_line(S0),
    read_line(T0),
    sorted_chars(S0, S),
    sorted_chars(T0, T),
    ( S == T -> Result = 1 ; Result = 0 ),
    format("~w~n", [Result]).