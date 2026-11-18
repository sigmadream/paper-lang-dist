main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    (   valid_anagram(S, T)
    ->  writeln(1)
    ;   writeln(0)
    ).

valid_anagram(S, T) :-
    string_length(S, L),
    string_length(T, L),
    string_codes(S, CS),
    string_codes(T, CT),
    msort(CS, SortedS),
    msort(CT, SortedT),
    SortedS == SortedT.