read_line_codes(Stream, Codes) :-
    read_line_to_codes(Stream, Raw),
    (   Raw == end_of_file
    ->  Codes = []
    ;   strip_trailing_cr(Raw, Codes)
    ).

strip_trailing_cr(Codes, Result) :-
    reverse(Codes, Rev),
    (   Rev = [13|Rest]
    ->  reverse(Rest, Result)
    ;   Result = Codes
    ).

main :-
    current_input(Stream),
    read_line_codes(Stream, S),
    read_line_codes(Stream, T),
    msort(S, SS),
    msort(T, TT),
    (   SS == TT
    ->  write(1)
    ;   write(0)
    ),
    nl.