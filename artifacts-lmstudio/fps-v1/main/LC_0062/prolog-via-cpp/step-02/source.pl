main :-
    read_line_to_string(Input),
    split_string(Input, ' ', '', [MStr, NStr]),
    string_to_integer(MStr, M),
    string_to_integer(NStr, N),
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