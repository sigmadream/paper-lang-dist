main :-
    (   read_line_to_string(user_input, S0),
        read_line_to_string(user_input, T0)
    ->  strip_cr(S0, S),
        strip_cr(T0, T),
        (   is_anagram(S, T)
        ->  write(1)
        ;   write(0)
        ),
        nl
    ;   true
    ).

strip_cr(S0, S) :-
    string_codes(S0, Codes0),
    (   append(Init, [13], Codes0)
    ->  string_codes(S, Init)
    ;   S = S0
    ).

is_anagram(S, T) :-
    string_length(S, L),
    string_length(T, L),
    string_codes(S, Cs),
    string_codes(T, Ct),
    msort(Cs, A),
    msort(Ct, B),
    A == B.