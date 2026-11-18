main :-
    read_string(user_input, "\n", "\r", _, S),
    read_string(user_input, "\n", "\r", _, T),
    string_codes(S, SC),
    string_codes(T, TC),
    msort(SC, SCS),
    msort(TC, TCS),
    ( SCS == TCS -> write(1) ; write(0) ),
    nl.