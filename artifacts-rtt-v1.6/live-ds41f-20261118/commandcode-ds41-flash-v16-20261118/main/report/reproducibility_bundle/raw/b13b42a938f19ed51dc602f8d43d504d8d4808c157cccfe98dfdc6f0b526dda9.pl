main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    string_codes(S, RawSC),
    string_codes(T, RawTC),
    delete(RawSC, 13, SC),
    delete(RawTC, 13, TC),
    msort(SC, SortedS),
    msort(TC, SortedT),
    ( SortedS == SortedT -> R = 1 ; R = 0 ),
    format("~w~n", [R]).