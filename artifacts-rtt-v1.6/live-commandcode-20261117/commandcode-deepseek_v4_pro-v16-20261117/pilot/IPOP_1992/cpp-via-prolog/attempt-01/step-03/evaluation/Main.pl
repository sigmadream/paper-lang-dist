:- module(main, [main/0]).

% Get character at position (R,C) in a grid represented as list of rows,
% each row is a list of single-character atoms (e.g., ['1','0']).
get_char(Grid, R, C, Char) :-
    nth0(R, Grid, Row),
    nth0(C, Row, Char).

% Check if all cells in the rectangle are the same as First.
check_uniform(Grid, R, C, Size, I, J, First) :-
    ( I >= R + Size ->
        true
    ; J >= C + Size ->
        I1 is I + 1,
        check_uniform(Grid, R, C, Size, I1, C, First)
    ; get_char(Grid, I, J, Ch),
      Ch == First,
      J1 is J + 1,
      check_uniform(Grid, R, C, Size, I, J1, First)
    ).

% Determine whether the given rectangle is uniform, and if so return its value.
uniform(Grid, R, C, Size, First) :-
    get_char(Grid, R, C, First),
    check_uniform(Grid, R, C, Size, R, C, First).

% Recursively compress the rectangle using quadtree decomposition.
compress(Grid, R, C, Size, Result) :-
    ( uniform(Grid, R, C, Size, First) ->
        Result = First
    ;
        Half is Size // 2,
        R1 is R + Half,
        C1 is C + Half,
        compress(Grid, R, C, Half, TL),
        compress(Grid, R, C1, Half, TR),
        compress(Grid, R1, C, Half, BL),
        compress(Grid, R1, C1, Half, BR),
        atom_concat('(', TL, T1),
        atom_concat(T1, TR, T2),
        atom_concat(T2, BL, T3),
        atom_concat(T3, BR, T4),
        atom_concat(T4, ')', Result)
    ).

% Read N lines from stdin and convert each into a list of char atoms.
read_grid_lines(0, []) :- !.
read_grid_lines(N, [Chars|Rest]) :-
    N > 0,
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Chars = []
    ;
        string_chars(Line, Chars)
    ),
    N1 is N - 1,
    read_grid_lines(N1, Rest).

main :-
    read_line_to_string(user_input, Line1),
    ( Line1 == end_of_file -> halt ; true ),
    string_trim(Line1, Trimmed1),
    number_string(N, Trimmed1),
    read_grid_lines(N, Grid),
    compress(Grid, 0, 0, N, Result),
    write(Result), nl.