main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        true
    ; strip_ws(Line, Clean),
      ( Clean == "" ->
          true
      ; atom_string(Atom, Clean),
        atom_number(Atom, N),
        print_bits(N)
      )
    ).

strip_ws(String, Clean) :-
    string_codes(String, Codes),
    remove_ws(Codes, CleanCodes),
    string_codes(Clean, CleanCodes).

remove_ws([], []).
remove_ws([C|Cs], Out) :-
    ( is_ws(C) ->
        remove_ws(Cs, Out)
    ; Out = [C|Out1],
      remove_ws(Cs, Out1)
    ).

is_ws(32).
is_ws(9).
is_ws(13).
is_ws(10).

print_bits(N) :-
    write(0),
    print_bits_from(1, N),
    nl.

print_bits_from(I, N) :-
    ( I > N ->
        true
    ; count_bits(I, C),
      write(' '),
      write(C),
      I1 is I + 1,
      print_bits_from(I1, N)
    ).

count_bits(N, C) :-
    count_bits(N, 0, C).

count_bits(0, Acc, Acc) :- !.
count_bits(N, Acc, C) :-
    B is N /\ 1,
    Acc1 is Acc + B,
    N1 is N >> 1,
    count_bits(N1, Acc1, C).