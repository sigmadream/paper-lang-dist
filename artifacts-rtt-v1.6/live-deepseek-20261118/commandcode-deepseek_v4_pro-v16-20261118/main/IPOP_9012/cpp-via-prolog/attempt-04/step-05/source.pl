main :-
    read_line_to_string(user_input, FirstLine),
    ( FirstLine = end_of_file ->
        true
    ; number_string(T, FirstLine),
      process_lines(T)
    ).

process_lines(0).
process_lines(T) :-
    T > 0,
    read_line_to_string(user_input, Line),
    ( Line = end_of_file ->
        true
    ; process_line(Line, Valid),
      ( Valid = true ->
          writeln('YES')
      ; writeln('NO')
      ),
      T1 is T - 1,
      process_lines(T1)
    ).

process_line(Line, Valid) :-
    string_chars(Line, Chars),
    process_chars(Chars, 0, 0, FinalBal, MinBal),
    ( MinBal >= 0, FinalBal =:= 0 ->
        Valid = true
    ; Valid = false
    ).

process_chars([], Bal, Min, Bal, Min).
process_chars([C|Cs], Bal, Min, FinalBal, FinalMin) :-
    ( C = '(' ->
        NewBal is Bal + 1
    ; C = ')' ->
        NewBal is Bal - 1
    ; NewBal = Bal
    ),
    NewMin is min(Min, NewBal),
    process_chars(Cs, NewBal, NewMin, FinalBal, FinalMin).