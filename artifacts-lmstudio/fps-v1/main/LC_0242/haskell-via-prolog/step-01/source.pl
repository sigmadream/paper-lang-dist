:- use_module(library(lists)).

frequencies([], []).
frequencies([X|XS], [(X, Count)|Freqs]) :-
    findall(X, member(X, XS), Same),
    length(Same, Count),
    remove_all(Same, XS, Remaining),
    frequencies(Remaining, Freqs).

remove_all(_, [], []) :- !.
remove_all(Elem, [Elem|Tail], Tail) :- !.
remove_all(Elem, [Head|Tail], [Head|NewTail]) :-
    remove_all(Elem, Tail, NewTail).

sort_string(S, Sorted) :-
    string_to_list(S, L),
    sort(L, SortedList),
    list_to_string(SortedList, Sorted).

main :-
    read_line_to_codes(user_input, Input1),
    string_to_atom(Input1, A),
    read_line_to_codes(user_input, Input2),
    string_to_atom(Input2, B),
    sort_string(A, SA),
    sort_string(B, SB),
    (frequencies(SA, FreqsA), frequencies(SB, FreqsB), FreqsA = FreqsB -> write(1); write(0)),
    nl.