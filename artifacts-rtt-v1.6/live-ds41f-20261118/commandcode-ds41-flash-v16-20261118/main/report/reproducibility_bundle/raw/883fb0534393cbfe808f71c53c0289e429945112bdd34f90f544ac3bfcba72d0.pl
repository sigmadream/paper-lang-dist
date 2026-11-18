main :-
    read_all_codes([], Rev),
    reverse(Rev, Codes),
    ( next_line(Codes, FirstLine, Rest, true) ->
        process_first(FirstLine, Rest)
    ; true
    ).

read_all_codes(Acc, Out) :-
    get_code(user_input, C),
    ( C =:= -1 ->
        Out = Acc
    ; read_all_codes([C|Acc], Out)
    ).

process_first(FirstLine, Rest) :-
    trim_codes(FirstLine, Trimmed),
    ( Trimmed == [] ->
        true
    ; ( catch(number_codes(T0, Trimmed), _, fail) ->
          ( integer(T0), T0 >= 0 ->
              read_print_lines(Rest, T0)
          ; true
          )
      ; true
      )
    ).

read_print_lines(_, 0) :- !.
read_print_lines(Codes, N) :-
    N > 0,
    ( next_line(Codes, Line0, Rest, true) ->
        strip_cr_codes(Line0, Line),
        ( valid_parentheses_codes(Line) ->
            writeln('YES')
        ; writeln('NO')
        ),
        N1 is N - 1,
        read_print_lines(Rest, N1)
    ; true
    ).

next_line([], [], [], false).
next_line(Codes, Line, Rest, true) :-
    Codes \== [],
    take_line_nonempty(Codes, Line, Rest).

take_line_nonempty([], [], []).
take_line_nonempty([10|Cs], [], Cs) :- !.
take_line_nonempty([C|Cs], [C|Line], Rest) :-
    take_line_nonempty(Cs, Line, Rest).

strip_cr_codes(Line, Stripped) :-
    reverse(Line, Rev),
    ( Rev = [13|RestRev] ->
        reverse(RestRev, Stripped)
    ; Stripped = Line
    ).

trim_codes(Codes, Trimmed) :-
    trim_left(Codes, L),
    reverse(L, RL),
    trim_left(RL, RLR),
    reverse(RLR, Trimmed).

trim_left([C|Cs], Out) :-
    is_space_code(C),
    !,
    trim_left(Cs, Out).
trim_left(Cs, Cs).

is_space_code(C) :-
    C =:= 32 ;
    C >= 9, C =< 13.

valid_parentheses_codes(Line) :-
    valid_codes(Line, 0).

valid_codes([], Bal) :-
    Bal =:= 0.
valid_codes([40|Rest], Bal) :-
    Bal1 is Bal + 1,
    valid_codes(Rest, Bal1).
valid_codes([41|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    valid_codes(Rest, Bal1).