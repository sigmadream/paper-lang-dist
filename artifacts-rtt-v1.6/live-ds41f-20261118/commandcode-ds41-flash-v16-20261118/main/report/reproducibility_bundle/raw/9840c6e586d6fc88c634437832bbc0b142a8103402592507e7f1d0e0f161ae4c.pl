:- use_module(library(readutil)).

main :-
    (   read_line_to_string(user_input, Line),
        Line \== end_of_file
    ->  strip_trailing_newline(Line, S),
        string_codes(S, Codes),
        reverse(Codes, RevCodes),
        (   Codes == RevCodes
        ->  format("1~n")
        ;   format("0~n")
        )
    ;   true
    ).

strip_trailing_newline(S0, S) :-
    string_codes(S0, Codes0),
    reverse(Codes0, Rev0),
    drop_trailing(Rev0, Rev),
    reverse(Rev, Codes),
    string_codes(S, Codes).

drop_trailing([13|T], R) :- !, drop_trailing(T, R).
drop_trailing([10|T], R) :- !, drop_trailing(T, R).
drop_trailing(L, L).