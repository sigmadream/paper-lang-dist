is_space(C) :-
    ( C =:= 32 ; C =:= 9 ; C =:= 13 ; C =:= 10 ).

count_bits(N, C) :-
    count_bits_(N, 0, C).

count_bits_(0, Acc, Acc) :- !.
count_bits_(N, Acc, C) :-
    N > 0,
    Acc1 is Acc + (N mod 2),
    N1 is N // 2,
    count_bits_(N1, Acc1, C).

write_bits_from(I, N) :-
    I =< N,
    !,
    write(' '),
    count_bits(I, C),
    write(C),
    I1 is I + 1,
    write_bits_from(I1, N).
write_bits_from(_, _).

main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        true
    ;
        exclude(is_space, Codes, Digits),
        number_codes(N, Digits),
        write(0),
        write_bits_from(1, N),
        nl
    ).