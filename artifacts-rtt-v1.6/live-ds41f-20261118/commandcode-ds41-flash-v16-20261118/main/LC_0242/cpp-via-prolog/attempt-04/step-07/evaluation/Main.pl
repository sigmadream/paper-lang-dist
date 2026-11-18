:- use_module(library(readutil)).

main :-
    (   read_line_to_string(user_input, S0),
        S0 \= end_of_file
    ->  (   read_line_to_string(user_input, T0),
            T0 \= end_of_file
        ->  strip_cr(S0, S),
            strip_cr(T0, T),
            (   string_length(S, L),
                string_length(T, L)
            ->  string_codes(S, Cs),
                string_codes(T, Ct),
                msort(Cs, Ss),
                msort(Ct, St),
                (   Ss == St
                ->  write(1), nl
                ;   write(0), nl
                )
            ;   write(0), nl
            )
        ;   true
        )
    ;   true
    ).

strip_cr(S0, S) :-
    string_codes(S0, Cs0),
    reverse(Cs0, Rev0),
    (   Rev0 = [13|RevRest]
    ->  reverse(RevRest, Cs),
        string_codes(S, Cs)
    ;   S = S0
    ).