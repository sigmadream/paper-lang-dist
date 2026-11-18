:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    Parts = [First|_],
    atom_number(First, N),
    numlist(0, N, Numbers),
    maplist(bit_count, Numbers, Counts),
    maplist(count_atom, Counts, Atoms),
    atomic_list_concat(Atoms, ' ', Out),
    writeln(Out).

bit_count(0, 0) :- !.
bit_count(N, C) :-
    N > 0,
    Half is N >> 1,
    bit_count(Half, C0),
    C is C0 + (N /\ 1).

count_atom(N, Atom) :-
    number_codes(N, Codes),
    atom_codes(Atom, Codes).