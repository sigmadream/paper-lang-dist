main :-
    read_integer(N),
    print_counts(0, N).

read_integer(N) :-
    current_input(Stream),
    skip_whitespace(Stream),
    read_digits(Stream, 0, N).

skip_whitespace(Stream) :-
    get_char(Stream, C),
    ( ( C == ' ' ; C == '\n' ; C == '\t' ; C == '\r' ) ->
        skip_whitespace(Stream)
    ;
        true
    ).

read_digits(Stream, Acc, N) :-
    get_char(Stream, C),
    ( C == end_of_file ->
        N = Acc
    ; char_code(C, Code),
      Code >= 48,
      Code =< 57 ->
        D is Code - 48,
        Acc1 is Acc * 10 + D,
        read_digits(Stream, Acc1, N)
    ;
        N = Acc
    ).

count_bits(X, Count) :-
    count_bits(X, 0, Count).

count_bits(0, Acc, Acc) :- !.
count_bits(X, Acc, Count) :-
    X > 0,
    Bit is X mod 2,
    Acc1 is Acc + Bit,
    X1 is X // 2,
    count_bits(X1, Acc1, Count).

print_counts(I, N) :-
    I =< N,
    count_bits(I, Count),
    ( I =:= 0 ->
        true
    ;
        write(' ')
    ),
    write(Count),
    I1 is I + 1,
    print_counts(I1, N).

print_counts(I, N) :-
    I > N,
    nl.