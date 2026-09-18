:- use_module(library(lists)).

sort_array(N, A) :-
    merge_sort(A, N, Sorted),
    print_list(Sorted).

merge_sort([], _, []).
merge_sort([X], _, [X]).
merge_sort(L, N, Sorted) :-
    split(L, N, Left, Right),
    merge_sort(Left, N1, SortedLeft),
    merge_sort(Right, N2, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

split([], _, [], []).
split([H|T], N, [H|Left], Right) :-
    N1 is N - 1,
    split(T, N1, Left, Right).

merge([], R, R).
merge(L, [], L).
merge([H1|T1], [H2|T2], [H1|Sorted]) :-
    H1 =< H2,
    merge(T1, [H2|T2], Sorted).
merge([H1|T1], [H2|T2], [H2|Sorted]) :-
    H1 > H2,
    merge([H1|T1], T2, Sorted).

print_list([]).
print_list([H|T]) :-
    write(H),
    (   T = [] -> true ; write(' '), print_list(T) ).

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, Chars),
    split_string(Chars, "\n", "", [NStr, AStr]),
    number_string(N, NStr),
    atom_codes(AAtom, AStr),
    atomic_list_concat(AAtoms, ' ', AAtom),
    maplist(atom_number, AAtoms, AList),
    length(AList, N),
    sort_array(N, AList),
    !.