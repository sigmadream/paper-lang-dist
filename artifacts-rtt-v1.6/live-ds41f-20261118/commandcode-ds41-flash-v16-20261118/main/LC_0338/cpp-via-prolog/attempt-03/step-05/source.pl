read_n(N) :-
    read_line_to_string(user_input, Line),
    Line \== end_of_file,
    split_string(Line, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [Token|_],
    number_string(N, Token).

main :-
    ( read_n(N) ->
        print_counts(N)
    ; true
    ).

print_counts(N) :-
    ( N >= 0 ->
        count_ones(0, C0),
        write(C0),
        print_counts_from(1, N)
    ; true
    ),
    nl.

print_counts_from(I, N) :-
    I > N, !.
print_counts_from(I, N) :-
    count_ones(I, C),
    write(' '),
    write(C),
    I1 is I + 1,
    print_counts_from(I1, N).

count_ones(0, 0) :- !.
count_ones(X, C) :-
    X > 0,
    B is X mod 2,
    X1 is X // 2,
    count_ones(X1, C1),
    C is C1 + B.