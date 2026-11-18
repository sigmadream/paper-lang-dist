main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   atom_codes(Atom, Codes),
        atom_number(Atom, N),
        findall(C, (between(0, N, I), count_bits(I, C)), Counts),
        print_counts(Counts)
    ).

count_bits(0, 0).
count_bits(X, C) :-
    X > 0,
    Y is X // 2,
    R is X mod 2,
    count_bits(Y, C0),
    C is C0 + R.

print_counts([]) :- nl.
print_counts([H|T]) :-
    write(H),
    print_counts_rest(T).

print_counts_rest([]) :- nl.
print_counts_rest([H|T]) :-
    write(' '),
    write(H),
    print_counts_rest(T).