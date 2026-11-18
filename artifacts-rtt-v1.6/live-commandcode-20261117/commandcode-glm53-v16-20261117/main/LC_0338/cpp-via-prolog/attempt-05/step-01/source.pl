:- module(main, [main/0]).
:- use_module(library(readutil)).

count_bits(N, Counts) :-
    length(Counts0, N1),
    N1 is N + 1,
    fill_counts(0, N, Counts0, Counts).

fill_counts(I, N, Acc, Acc) :- I > N, !.
fill_counts(I, N, Acc, Out) :-
    ( I =:= 0 -> C = 0
    ; H is I // 2, nth0(H, Acc, HC), C is HC + I mod 2 ),
    nth0(I, Acc, _, Acc2, C),
    I1 is I + 1,
    fill_counts(I1, N, Acc2, Out).

join(List, Atom) :-
    maplist(number_codes, List, CodesList),
    interleave_space(CodesList, Codes),
    flatten(Codes, Flat),
    atom_codes(Atom, Flat).

interleave_space([], []).
interleave_space([X], [X]).
interleave_space([X,Y|T], [X, [32], R]) :-
    interleave_space([Y|T], R).

main :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file -> N = 0
    ; number_codes(N, Line)
    ),
    count_bits(N, Counts),
    join(Counts, Atom),
    write(Atom), nl.