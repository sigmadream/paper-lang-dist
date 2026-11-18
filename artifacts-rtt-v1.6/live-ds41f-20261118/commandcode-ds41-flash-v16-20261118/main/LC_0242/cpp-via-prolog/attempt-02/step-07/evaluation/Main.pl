main :-
    read_line_safe(S),
    read_line_safe(T),
    string_codes(S, SCodes),
    string_codes(T, TCodes),
    clean_codes(SCodes, SClean),
    clean_codes(TCodes, TClean),
    msort(SClean, SSorted),
    msort(TClean, TSorted),
    ( SSorted == TSorted -> Result = 1 ; Result = 0 ),
    write(Result),
    nl.

read_line_safe(Line) :-
    ( read_line_to_string(user_input, L) ->
        ( L == end_of_file -> Line = "" ; Line = L )
    ;
        Line = ""
    ).

clean_codes([], []).
clean_codes([C|Cs], Result) :-
    ( is_whitespace(C) ->
        clean_codes(Cs, Result)
    ;
        Result = [C|Rest],
        clean_codes(Cs, Rest)
    ).

is_whitespace(32).
is_whitespace(9).
is_whitespace(10).
is_whitespace(13).