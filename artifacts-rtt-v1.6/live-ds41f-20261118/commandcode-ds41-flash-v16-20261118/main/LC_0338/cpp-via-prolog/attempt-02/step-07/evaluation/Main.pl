count_bits(0, 0).
count_bits(N, C) :-
    N > 0,
    N1 is N >> 1,
    count_bits(N1, C1),
    C is C1 + (N /\ 1).

print_from(I, N) :- I > N, !.
print_from(I, N) :-
    count_bits(I, C),
    format(" ~w", [C]),
    I1 is I + 1,
    print_from(I1, N).

print_bits(N) :-
    format("0", []),
    print_from(1, N),
    nl.

main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> true
    ; split_string(Line, "", " \t\r\n", Parts),
      Parts = [First|_],
      number_string(N, First),
      print_bits(N)
    ).