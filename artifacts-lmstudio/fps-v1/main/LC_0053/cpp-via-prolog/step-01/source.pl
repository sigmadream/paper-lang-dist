:- use_module(library(readutil)).
:- set_prolog_flag(double_quotes, chars).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, InputList),
    split_string(InputList, " ", "", InputParts),
    maplist(string_to_integer, InputParts, Numbers),
    nth0(1, Numbers, N),
    nth0(2, Numbers, A),
    find_max_subarray(N, A, Result),
    write(Result),
    nl.

find_max_subarray(_, [], 0).
find_max_subarray(N, [H|T], Result) :-
    find_max_subarray_helper(H, T, H, H, N, Result).

find_max_subarray_helper(CurrentMax, [], CurrentMax, BestSoFar, _, BestSoFar).
find_max_subarray_helper(CurrentMax, [H|T], NewCurrentMax, BestSoFar, N, Result) :-
    NewCurrentMax is max(H, CurrentMax + H),
    BestSoFar1 is max(BestSoFar, NewCurrentMax),
    find_max_subarray_helper(NewCurrentMax, T, NewCurrentMax, BestSoFar1, N, Result).