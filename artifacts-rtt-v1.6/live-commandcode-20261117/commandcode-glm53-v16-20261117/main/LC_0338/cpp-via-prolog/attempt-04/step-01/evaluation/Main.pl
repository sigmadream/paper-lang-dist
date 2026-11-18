:- module(main, []).
:- use_module(library(readutil)).

count_bits(0, C, [C]) :- !.
count_bits(I, C, [C|Rest]) :-
    C1 is C + I mod 2,
    I1 is I - 1,
    count_bits(I1, C1, Rest).

build(N, List) :- count_bits(N, 0, List).

print_list([]) :- nl.
print_list([X]) :- !, format("~w~n", [X]).
print_list([X|T]) :-
    format("~w ", [X]),
    print_list(T).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    ( Line == end_of_file -> N = 0
    ; split_string(Line, " \t", " \t", Parts),
      ( Parts == [] -> N = 0
      ; nth0(0, Parts, P),
        atom_number(P, N)
      )
    ),
    build(N, List),
    print_list(List).