:- use_module(library(readutil)).
:- use_module(library(lists)).

max_subarray_sum(N, Xs) :-
    nth0(0, Xs, First),
    foldl'(step, Xs, (First, First), (_, Best)),
    print(Best).

step((Ending, Best), X, (Next, NewBest)) :-
    Next is max(X, Ending + X),
    NewBest is max(Best, Next).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, StrList),
    maplist(atom_number, StrList, NumList),
    nth0(0, NumList, N),
    nth1(N, NumList, Xs),
    max_subarray_sum(N, Xs).