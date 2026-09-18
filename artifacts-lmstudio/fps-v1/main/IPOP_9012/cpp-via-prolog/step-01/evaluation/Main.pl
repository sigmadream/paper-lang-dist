main :-
    read_line_to_string(Input),
    string_to_list(Input, Chars),
    maplist(process_line, Chars).

process_line(Line) :-
    string_to_list(Line, Chars),
    check_balance(Chars, 0, Valid),
    (   Valid -> write('YES'), nl ; write('NO'), nl ).

check_balance([], _, true).
check_balance([H|T], Bal, Valid) :-
    (   H = '(' -> NewBal is Bal + 1 ;
        H = ')' -> NewBal is Bal - 1
    ),
    (   NewBal < 0 -> Valid = false ; true ),
    check_balance(T, NewBal, Valid).