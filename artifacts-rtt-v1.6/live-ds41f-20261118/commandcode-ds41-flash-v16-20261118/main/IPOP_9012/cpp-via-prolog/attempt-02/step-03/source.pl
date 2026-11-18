main :-
    read_line_to_string(current_input, TLine),
    (   TLine == end_of_file
    ->  true
    ;   split_string(TLine, "", " \t\r\n", [TStr|_]),
        number_string(T, TStr),
        process(T)
    ).

process(0) :- !.
process(N) :-
    read_line_to_string(current_input, Line),
    (   Line == end_of_file
    ->  true
    ;   check_balanced(Line, Result),
        write_result(Result),
        N1 is N - 1,
        process(N1)
    ).

check_balanced(Line, Result) :-
    string_chars(Line, Chars),
    check_chars(Chars, 0, Result).

check_chars([], Balance, Result) :-
    (   Balance =:= 0
    ->  Result = yes
    ;   Result = no
    ).
check_chars(['('|Rest], Balance, Result) :-
    Next is Balance + 1,
    check_chars(Rest, Next, Result).
check_chars([')'|Rest], Balance, Result) :-
    (   Balance =:= 0
    ->  Result = no
    ;   Next is Balance - 1,
        check_chars(Rest, Next, Result)
    ).
check_chars([_|Rest], Balance, Result) :-
    check_chars(Rest, Balance, Result).

write_result(yes) :-
    writeln('YES').
write_result(no) :-
    writeln('NO').