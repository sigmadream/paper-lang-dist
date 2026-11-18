:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, chars).

main :-
    read_line_to_codes(user_input, Line1),
    ( Line1 == end_of_file -> true
    ; atom_codes(TA, Line1),
      atom_number(TA, T),
      read_line_to_codes(user_input, _),
      process(T),
      fail
    ; true ).

process(0) :- !.
process(N) :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file -> true
    ; check(Line, Valid),
      ( Valid == true -> write("YES\n") ; write("NO\n") ),
      N1 is N - 1,
      process(N1)
    ).

check(Line, Result) :-
    check_line(Line, 0, R),
    ( R == 0 -> Result = true ; Result = false ).

check_line([], Bal, Bal).
check_line([0'(|Rest], Bal0, Bal) :- !,
    Bal1 is Bal0 + 1,
    Bal1 >= 0,
    check_line(Rest, Bal1, Bal).
check_line([0')|Rest], Bal0, Bal) :- !,
    Bal1 is Bal0 - 1,
    Bal1 >= 0,
    check_line(Rest, Bal1, Bal).
check_line(_, _, -1).