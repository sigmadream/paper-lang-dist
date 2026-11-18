strip_trailing_cr(Codes, Result) :-
    reverse(Codes, Rev),
    strip_leading_cr(Rev, Rev2),
    reverse(Rev2, Result).

strip_leading_cr([13|T], R) :-
    !,
    strip_leading_cr(T, R).
strip_leading_cr(C, C).

strip_cr(S, T) :-
    string_codes(S, Codes),
    strip_trailing_cr(Codes, Codes2),
    string_codes(T, Codes2).

process(S) :-
    strip_cr(S, T),
    string_codes(T, Codes),
    reverse(Codes, Rev),
    (   Codes == Rev
    ->  R = 1
    ;   R = 0
    ),
    format("~w~n", [R]).

main :-
    (   read_line_to_string(user_input, S)
    ->  (   S == end_of_file
        ->  true
        ;   process(S)
        )
    ;   true
    ).