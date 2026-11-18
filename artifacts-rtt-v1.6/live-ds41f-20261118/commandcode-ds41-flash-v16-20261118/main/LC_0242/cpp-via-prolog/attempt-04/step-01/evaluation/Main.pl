main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    string_codes(S, CS),
    string_codes(T, CT),
    msort(CS, SortedS),
    msort(CT, SortedT),
    ( SortedS == SortedT -> Result = 1 ; Result = 0 ),
    writeln(Result).