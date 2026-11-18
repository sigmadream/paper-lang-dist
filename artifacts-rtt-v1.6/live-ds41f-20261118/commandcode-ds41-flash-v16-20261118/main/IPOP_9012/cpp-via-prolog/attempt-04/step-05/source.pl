space_code(9).
space_code(10).
space_code(11).
space_code(12).
space_code(13).
space_code(32).

is_space_code(C) :-
    space_code(C).

reverse_codes(Xs, Ys) :-
    reverse_codes(Xs, [], Ys).

reverse_codes([], Acc, Acc).
reverse_codes([X|Xs], Acc, Ys) :-
    reverse_codes(Xs, [X|Acc], Ys).

drop_leading_space([C|Cs], Rest) :-
    is_space_code(C),
    !,
    drop_leading_space(Cs, Rest).
drop_leading_space(Cs, Cs).

trim_string(String, Trimmed) :-
    string_codes(String, Codes),
    drop_leading_space(Codes, Codes1),
    reverse_codes(Codes1, Rev1),
    drop_leading_space(Rev1, Rev2),
    reverse_codes(Rev2, TrimmedCodes),
    string_codes(Trimmed, TrimmedCodes).

valid_parens(String, Ok) :-
    string_codes(String, Codes),
    valid_codes(Codes, 0, Ok).

valid_codes([], Balance, Ok) :-
    ( Balance =:= 0 ->
        Ok = true
    ;
        Ok = false
    ).
valid_codes([C|Cs], Balance, Ok) :-
    ( C =:= 40 ->
        B1 is Balance + 1,
        valid_codes(Cs, B1, Ok)
    ; C =:= 41 ->
        ( Balance > 0 ->
            B1 is Balance - 1,
            valid_codes(Cs, B1, Ok)
        ;
            Ok = false
        )
    ;
        valid_codes(Cs, Balance, Ok)
    ).

main :-
    read_line_to_string(user_input, FirstLine),
    ( FirstLine == end_of_file ->
        true
    ;
        trim_string(FirstLine, TrimmedFirstLine),
        ( number_string(T, TrimmedFirstLine) ->
            process(T)
        ;
            true
        )
    ).

process(0) :-
    !.
process(N) :-
    N > 0,
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        true
    ;
        trim_string(Line, TrimmedLine),
        ( valid_parens(TrimmedLine, true) ->
            write('YES'), nl
        ;
            write('NO'), nl
        ),
        N1 is N - 1,
        process(N1)
    ).