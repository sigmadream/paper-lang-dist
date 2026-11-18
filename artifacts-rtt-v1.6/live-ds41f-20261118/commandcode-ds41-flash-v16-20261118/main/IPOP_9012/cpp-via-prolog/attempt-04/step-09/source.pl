main :-
    current_input(Stream),
    read_line_to_string(Stream, Line0),
    ( Line0 == end_of_file ->
        true
    ; trim_string(Line0, First),
      ( parse_int(First, T) ->
          process(T, Stream)
      ; true
      )
    ).

process(0, _) :- !.
process(N, Stream) :-
    N > 0,
    read_line_to_string(Stream, Line),
    ( Line == end_of_file ->
        true
    ; trim_string(Line, Trimmed),
      ( valid_parens(Trimmed) ->
          writeln('YES')
      ; writeln('NO')
      ),
      N1 is N - 1,
      process(N1, Stream)
    ).

parse_int(Str, T) :-
    catch(number_string(T, Str), _, fail).

valid_parens(Str) :-
    string_codes(Str, Codes),
    valid_balance(Codes, 0).

valid_balance([], 0).
valid_balance([40|Rest], B) :-
    B1 is B + 1,
    valid_balance(Rest, B1).
valid_balance([41|Rest], B) :-
    B > 0,
    B1 is B - 1,
    valid_balance(Rest, B1).
valid_balance([C|Rest], B) :-
    C =\= 40,
    C =\= 41,
    valid_balance(Rest, B).

trim_string(Str, Trimmed) :-
    string_codes(Str, Codes),
    trim_left(Codes, LeftTrimmed),
    reverse(LeftTrimmed, Rev),
    trim_left(Rev, RevTrimmed),
    reverse(RevTrimmed, Final),
    string_codes(Trimmed, Final).

trim_left([C|Rest], Result) :-
    is_ws_code(C), !,
    trim_left(Rest, Result).
trim_left(Rest, Rest).

is_ws_code(9).
is_ws_code(10).
is_ws_code(11).
is_ws_code(12).
is_ws_code(13).
is_ws_code(32).