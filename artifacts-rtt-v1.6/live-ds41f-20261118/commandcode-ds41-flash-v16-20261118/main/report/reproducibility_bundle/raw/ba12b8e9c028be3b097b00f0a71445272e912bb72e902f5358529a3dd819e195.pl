remove_cr([], []).
remove_cr([13|T], R) :-
    remove_cr(T, R).
remove_cr([H|T], [H|R]) :-
    H \= 13,
    remove_cr(T, R).

main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    string_codes(S, SC),
    string_codes(T, TC),
    remove_cr(SC, SClean),
    remove_cr(TC, TClean),
    msort(SClean, SSorted),
    msort(TClean, TSorted),
    (   SSorted == TSorted
    ->  Result = 1
    ;   Result = 0
    ),
    writeln(Result).