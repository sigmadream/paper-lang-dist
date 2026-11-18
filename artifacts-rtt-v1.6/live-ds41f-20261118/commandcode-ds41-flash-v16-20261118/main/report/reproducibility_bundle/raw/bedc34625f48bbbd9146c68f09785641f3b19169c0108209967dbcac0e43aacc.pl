strip_cr(Str, Codes) :-
    string_codes(Str, Raw),
    reverse(Raw, Rev),
    (   Rev = [13|Rest]
    ->  reverse(Rest, Codes)
    ;   Codes = Raw
    ).

main :-
    read_line_to_string(user_input, SStr),
    read_line_to_string(user_input, TStr),
    strip_cr(SStr, SCodes),
    strip_cr(TStr, TCodes),
    msort(SCodes, SSorted),
    msort(TCodes, TSorted),
    (   SSorted == TSorted
    ->  Result = 1
    ;   Result = 0
    ),
    writeln(Result).