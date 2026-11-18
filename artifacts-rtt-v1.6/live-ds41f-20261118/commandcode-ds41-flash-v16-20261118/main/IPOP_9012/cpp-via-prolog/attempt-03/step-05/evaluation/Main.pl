:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, FirstLine),
    ( FirstLine == end_of_file
    -> true
    ; trim_string(FirstLine, TStr),
      atom_string(TAtom, TStr),
      atom_number(TAtom, T),
      process_cases(T)
    ).

process_cases(0) :- !.
process_cases(N) :-
    N > 0,
    read_line_to_string(user_input, Line),
    ( Line == end_of_file
    -> true
    ; trim_string(Line, S),
      ( valid_parens(S) -> writeln('YES') ; writeln('NO') ),
      N1 is N - 1,
      process_cases(N1)
    ).

trim_string(S, T) :-
    string_codes(S, Codes),
    trim_left(Codes, Codes1),
    reverse(Codes1, RevCodes1),
    trim_left(RevCodes1, RevCodes2),
    reverse(RevCodes2, TCodes),
    string_codes(T, TCodes).

trim_left([C|Cs], Rest) :-
    is_space_code(C),
    !,
    trim_left(Cs, Rest).
trim_left(Cs, Cs).

is_space_code(C) :-
    ( C =:= 9
    ; C =:= 10
    ; C =:= 11
    ; C =:= 12
    ; C =:= 13
    ; C =:= 32
    ).

valid_parens(S) :-
    string_codes(S, Cs),
    Cs = [_|_],
    valid_parens_codes(Cs, 0, Balance),
    Balance =:= 0.

valid_parens_codes([], B, B).
valid_parens_codes([40|Cs], B, Final) :-
    B1 is B + 1,
    valid_parens_codes(Cs, B1, Final).
valid_parens_codes([41|Cs], B, Final) :-
    B > 0,
    B1 is B - 1,
    valid_parens_codes(Cs, B1, Final).