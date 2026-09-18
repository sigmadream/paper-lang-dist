:- use_module(library(readutil)).
:- set_prolog_flag(double_quotes, chars).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, InputList),
    split_string(InputList, " ", "", InputParts),
    maplist(atom_number, InputParts, Numbers),
    length(Numbers, N),
    move_zeroes(N, Numbers, Result),
    print_result(Result).

move_zeroes(_, [], []).
move_zeroes(N, [H|T], Result) :-
    H =\= 0,
    move_zeroes(N-1, T, Tail),
    append([H], Tail, Result).
move_zeroes(N, [0|T], Result) :-
    N > 0,
    move_zeroes(N-1, T, Tail),
    append([0], Tail, Result).

print_result([]).
print_result([H|T]) :-
    write(H),
    (   T = []
    ->  true
    ;   write(' '),
        print_result(T)
    ),
    nl.