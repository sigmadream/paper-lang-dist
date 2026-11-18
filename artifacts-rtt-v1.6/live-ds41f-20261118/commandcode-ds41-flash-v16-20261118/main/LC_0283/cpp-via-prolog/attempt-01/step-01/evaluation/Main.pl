main :-
    read_all_codes(Codes),
    string_codes(Input, Codes),
    split_string(Input, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [NTok|Rest],
    number_string(N, NTok),
    take_numbers(N, Rest, A),
    move_zeroes(A, Result),
    print_values(Result).

read_all_codes(Codes) :-
    read_all_codes_acc([], RevCodes),
    reverse(RevCodes, Codes).

read_all_codes_acc(Acc, Codes) :-
    get_char(user_input, C),
    ( C == end_of_file ->
        Codes = Acc
    ; char_code(C, Code),
      read_all_codes_acc([Code|Acc], Codes)
    ).

take_numbers(0, _, []) :- !.
take_numbers(N, [T|Ts], [X|Xs]) :-
    N > 0,
    number_string(X, T),
    N1 is N - 1,
    take_numbers(N1, Ts, Xs).

move_zeroes(A, R) :-
    move_zeroes_acc(A, NZRev, ZRev),
    reverse(NZRev, NZ),
    reverse(ZRev, Z),
    append(NZ, Z, R).

move_zeroes_acc([], [], []).
move_zeroes_acc([X|Xs], NZ, Z) :-
    ( X =:= 0 ->
        Z = [X|Z1],
        move_zeroes_acc(Xs, NZ, Z1)
    ;   NZ = [X|NZ1],
        move_zeroes_acc(Xs, NZ1, Z)
    ).

print_values([]) :- nl.
print_values([X|Xs]) :-
    write(X),
    print_tail(Xs).

print_tail([]) :- nl.
print_tail([X|Xs]) :-
    write(' '),
    write(X),
    print_tail(Xs).