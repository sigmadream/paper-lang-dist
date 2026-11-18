main :-
    read_line_to_string(user_input, TLine0),
    ( TLine0 == end_of_file ->
        true
    ; trim_string(TLine0, TStr),
      number_string(T, TStr),
      process(T)
    ).

trim_string(S0, S) :-
    split_string(S0, "", " \t\r\n", [S]).

process(0) :- !.
process(N) :-
    read_line_to_string(user_input, Line0),
    ( Line0 == end_of_file ->
        true
    ; trim_string(Line0, Line),
      check_line(Line),
      N1 is N - 1,
      process(N1)
    ).

check_line(Line) :-
    string_codes(Line, Codes),
    balance(Codes, 0, Ok),
    ( Ok == true -> writeln('YES') ; writeln('NO') ).

balance([], Bal, Ok) :-
    ( Bal =:= 0 -> Ok = true ; Ok = false ).
balance([C|Cs], Bal, Ok) :-
    ( C =:= 40 ->
        Bal1 is Bal + 1,
        balance(Cs, Bal1, Ok)
    ; ( C =:= 41 ->
          ( Bal > 0 ->
              Bal1 is Bal - 1,
              balance(Cs, Bal1, Ok)
          ; Ok = false
          )
      ; balance(Cs, Bal, Ok)
      )
    ).