:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, S),
    ( S == end_of_file -> N = 0 ; number_string(N, S) ),
    format('~w', [0]),
    print_bits(1, N),
    nl.

print_bits(I, N) :-
    I > N, !.
print_bits(I, N) :-
    count_bits(I, C),
    format(' ~w', [C]),
    I1 is I + 1,
    print_bits(I1, N).

count_bits(0, 0) :- !.
count_bits(N, C) :-
    N > 0,
    B is N /\ 1,
    N1 is N >> 1,
    count_bits(N1, C1),
    C is C1 + B.