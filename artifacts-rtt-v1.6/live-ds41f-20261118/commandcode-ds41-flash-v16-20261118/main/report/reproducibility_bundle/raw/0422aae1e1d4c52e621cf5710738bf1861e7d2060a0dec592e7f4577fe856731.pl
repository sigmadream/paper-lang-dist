main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        N = 0
    ;
        parse_line(Line, N)
    ),
    print_counts(N).

parse_line(Line, N) :-
    string_chars(Line, Chars),
    include(valid_char, Chars, Filtered),
    ( Filtered = [] ->
        N = 0
    ;
        maplist(char_code, Filtered, Codes),
        ( catch(number_codes(N0, Codes), _, fail) ->
            N = N0
        ;
            N = 0
        )
    ).

valid_char(C) :-
    C == '-' ;
    ( C >= '0',
      C =< '9'
    ).

print_counts(N) :-
    forall(
        between(0, N, I),
        (
            ( I > 0 -> write(' ') ; true ),
            count_bits(I, C),
            write(C)
        )
    ),
    nl.

count_bits(N, C) :-
    count_bits(N, 0, C).

count_bits(0, Acc, Acc) :- !.
count_bits(N, Acc, C) :-
    N > 0,
    Acc1 is Acc + (N mod 2),
    M is N // 2,
    count_bits(M, Acc1, C).