main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   (   parse_n(Line, N)
        ->  print_counts(0, N),
            nl
        ;   true
        )
    ).

parse_n(Line, N) :-
    split_string(Line, " \t\r\n", " \t\r\n", [Token|_]),
    Token \== "",
    number_string(N, Token).

print_counts(I, N) :-
    I =< N,
    count_bits(I, C),
    (   I > 0
    ->  write(' ')
    ;   true
    ),
    write(C),
    Next is I + 1,
    print_counts(Next, N).
print_counts(I, N) :-
    I > N.

count_bits(0, 0) :- !.
count_bits(X, C) :-
    X > 0,
    X1 is X // 2,
    count_bits(X1, C1),
    C is C1 + (X mod 2).