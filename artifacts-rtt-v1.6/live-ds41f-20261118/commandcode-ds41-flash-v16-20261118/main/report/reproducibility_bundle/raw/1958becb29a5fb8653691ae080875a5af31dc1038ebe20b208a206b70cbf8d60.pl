ws(C) :- C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 13.

main :-
    read_line_to_string(user_input, SRead),
    read_line_to_string(user_input, TRead),
    ( SRead == end_of_file -> S = "" ; S = SRead ),
    ( TRead == end_of_file -> T = "" ; T = TRead ),
    string_codes(S, SCodes),
    string_codes(T, TCodes),
    exclude(ws, SCodes, SClean),
    exclude(ws, TCodes, TClean),
    msort(SClean, SSorted),
    msort(TClean, TSorted),
    ( SSorted == TSorted -> write(1) ; write(0) ),
    nl.