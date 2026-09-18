binary_search(N, Target, Arr, Result) :-
    binary_search_helper(0, N-1, Arr, Target, Result).

binary_search_helper(L, R, _, Target, Index) :-
    L > R,
    Index = -1.
binary_search_helper(L, R, Arr, Target, Index) :-
    Mid is (L + R) // 2,
    nth0(Mid, Arr, MidValue),
    MidValue =:= Target,
    Index = Mid.
binary_search_helper(L, R, Arr, Target, Index) :-
    Mid is (L + R) // 2,
    nth0(Mid, Arr, MidValue),
    MidValue < Target,
    NewL is Mid + 1,
    binary_search_helper(NewL, R, Arr, Target, Index).
binary_search_helper(L, R, Arr, Target, Index) :-
    Mid is (L + R) // 2,
    nth0(Mid, Arr, MidValue),
    MidValue > Target,
    NewR is Mid - 1,
    binary_search_helper(L, NewR, Arr, Target, Index).

main :-
    read_line_to_string(_, Input),
    split_string(Input, ' ', '', Parts),
    maplist(atom_number, Parts, [N, T | Arr]),
    length(Arr, N),
    binary_search(N, T, Arr, Result),
    write(Result), nl.