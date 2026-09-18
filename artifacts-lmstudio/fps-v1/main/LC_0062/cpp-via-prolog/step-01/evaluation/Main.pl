:- use_module(library(readutil)).
:- use_module(library(write)).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, InputList),
    split_string(InputList, ' ', '', [MStr, NStr]),
    number_string(M, MStr),
    number_string(N, NStr),
    unique_paths(M, N, Result),
    write(Result),
    nl.

unique_paths(1, _, 1) :- !.
unique_paths(_, 1, 1) :- !.
unique_paths(M, N, Result) :-
    M > 1,
    N > 1,
    M1 is M - 1,
    N1 is N - 1,
    unique_paths(M1, N, PathsUp),
    unique_paths(M, N1, PathsLeft),
    Result is PathsUp + PathsLeft.