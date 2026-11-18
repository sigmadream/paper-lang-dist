:- module(main, []).
:- use_module(library(apply)).
:- use_module(library(dcg/basics)).

main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> N = 0
    ; phrase(number(N), L1, _) ),
    read_line_to_codes(user_input, L2),
    ( L2 == end_of_file -> Vals = []
    ; phrase(parse_ints(Vals), L2) ),
    length(Vals, N),
    partition_nonzeros(Vals, NonZeros, Zeros),
    append(NonZeros, Zeros, Result),
    print_ints(Result).

partition_nonzeros([], [], []).
partition_nonzeros([V|Vs], NonZeros, Zeros) :-
    ( V =\= 0 ->
        NonZeros = [V|R1], Zeros = R2
    ;   NonZeros = R1, Zeros = [0|R2]
    ),
    partition_nonzeros(Vs, R1, R2).

print_ints([]) :- nl.
print_ints([V|Vs]) :-
    write(V),
    ( Vs == [] -> true ; write(' ') ),
    print_ints(Vs).

number(N) --> integer(N).
number(N) --> blanks, integer(N).

parse_ints([]) --> [].
parse_ints([V|Vs]) --> blanks, integer(V), parse_ints(Vs).