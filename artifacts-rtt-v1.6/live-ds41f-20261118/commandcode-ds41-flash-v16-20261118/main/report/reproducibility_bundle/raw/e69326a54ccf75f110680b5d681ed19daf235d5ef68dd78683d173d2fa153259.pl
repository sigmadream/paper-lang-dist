main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", [Token|_]),
    atom_string(Atom, Token),
    atom_number(Atom, N),
    print_counts(N).

print_counts(N) :-
    format('~d', [0]),
    print_from(1, N).

print_from(I, N) :-
    (   I > N
    ->  nl
    ;   popcount(I, C),
        format(' ~d', [C]),
        J is I + 1,
        print_from(J, N)
    ).

popcount(N, C) :-
    popcount_(N, 0, C).

popcount_(0, Acc, Acc) :- !.
popcount_(X, Acc, C) :-
    Acc1 is Acc + (X /\ 1),
    X1 is X >> 1,
    popcount_(X1, Acc1, C).