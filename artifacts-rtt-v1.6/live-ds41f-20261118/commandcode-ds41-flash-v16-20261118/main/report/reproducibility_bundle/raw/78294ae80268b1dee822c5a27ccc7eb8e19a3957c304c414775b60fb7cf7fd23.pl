main :-
    ( read_line_to_codes(user_input, FirstCodes),
      FirstCodes \== end_of_file ->
        trim_codes(FirstCodes, TCodes),
        ( TCodes == [] ->
            true
        ; ( catch(number_codes(T, TCodes), _, fail) ->
              loop(T)
          ; true
          )
        )
    ; true
    ).

loop(0) :- !.
loop(N) :-
    N > 0,
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file ->
        true
    ; trim_codes(Line, S),
      ( valid_parens(S) ->
          writeln('YES')
      ; writeln('NO')
      ),
      N1 is N - 1,
      loop(N1)
    ).

trim_codes(Codes, Trimmed) :-
    strip_leading_ws(Codes, C1),
    reverse(C1, R1),
    strip_leading_ws(R1, R2),
    reverse(R2, Trimmed).

strip_leading_ws([C|Cs], Rest) :-
    whitespace(C),
    !,
    strip_leading_ws(Cs, Rest).
strip_leading_ws(Cs, Cs).

whitespace(C) :-
    C =:= 9
    ; C =:= 10
    ; C =:= 11
    ; C =:= 12
    ; C =:= 13
    ; C =:= 32.

valid_parens(Codes) :-
    Codes \== [],
    valid(Codes, 0).

valid([], 0).
valid([40|Cs], Bal) :-
    Bal1 is Bal + 1,
    valid(Cs, Bal1).
valid([41|Cs], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    valid(Cs, Bal1).