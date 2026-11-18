main :-
    read_line_to_string(user_input, FirstLine),
    ( FirstLine == end_of_file -> true
    ; split_string(FirstLine, " \t\r\n", " \t\r\n", Tokens),
      Tokens = [TStr|_],
      string_codes(TStr, Codes),
      number_codes(T, Codes),
      process_lines(T)
    ).

process_lines(0) :- !.
process_lines(N) :-
    N > 0,
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> true
    ; check_balanced(Line, Ok),
      ( Ok == true -> writeln('YES') ; writeln('NO') ),
      N1 is N - 1,
      process_lines(N1)
    ).

check_balanced(Str, Ok) :-
    string_chars(Str, Chars),
    check_balance(Chars, 0, Ok).

check_balance([], Bal, Ok) :-
    ( Bal =:= 0 -> Ok = true ; Ok = false ).
check_balance(['('|Rest], Bal, Ok) :-
    Bal1 is Bal + 1,
    check_balance(Rest, Bal1, Ok).
check_balance([')'|Rest], Bal, Ok) :-
    Bal > 0,
    Bal1 is Bal - 1,
    check_balance(Rest, Bal1, Ok).
check_balance([')'|_], 0, false) :- !.
check_balance([_|Rest], Bal, Ok) :-
    check_balance(Rest, Bal, Ok).