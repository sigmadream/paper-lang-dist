read_first_int(N) :-
    get_char(user_input, C),
    ( char_type(C, digit) ->
        C0 is C - 0'0,
        read_int_digits(C0, N)
    ;   read_first_int(N)
    ).

read_int_digits(Acc, N) :-
    get_char(user_input, C),
    ( char_type(C, digit) ->
        D is C - 0'0,
        Acc1 is Acc * 10 + D,
        read_int_digits(Acc1, N)
    ;   N = Acc
    ).

bit_count(0, 0) :- !.
bit_count(X, C) :-
    X > 0,
    X1 is X // 2,
    R is X mod 2,
    bit_count(X1, C1),
    C is C1 + R.

print_counts(I, N) :-
    I > N,
    !,
    nl.
print_counts(I, N) :-
    bit_count(I, C),
    ( I =:= 0 -> true ; write(' ') ),
    write(C),
    I1 is I + 1,
    print_counts(I1, N).

main :-
    read_first_int(N),
    print_counts(0, N).