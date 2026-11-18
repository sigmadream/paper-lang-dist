strip_trailing_cr(S0, S) :-
    string_codes(S0, Codes0),
    (   append(Codes, [13], Codes0)
    ->  string_codes(S, Codes)
    ;   S = S0
    ).

read_line_codes(S) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  S = ""
    ;   strip_trailing_cr(Line, S)
    ).

is_anagram(S, T) :-
    string_codes(S, CodesS0),
    msort(CodesS0, CodesS),
    string_codes(T, CodesT0),
    msort(CodesT0, CodesT),
    CodesS == CodesT.

main :-
    read_line_codes(S),
    read_line_codes(T),
    (   is_anagram(S, T)
    ->  writeln(1)
    ;   writeln(0)
    ).