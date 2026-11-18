:- module(main, [main/0]).
:- use_module(library(readutil)).
:- use_module(library(lists)).

% Remove trailing carriage return if present
clean_line(Line, Clean) :-
    string_length(Line, Len),
    ( Len > 0,
      sub_string(Line, Len1, 1, 0, "\r"),
      Len1 is Len - 1
    -> sub_string(Line, 0, Len1, 0, Clean)
    ;  Clean = Line
    ).

% Check if all characters in the sub-grid are the same
same_region(Grid, R, C, Size) :-
    Size > 0,
    R_end is R + Size - 1,
    C_end is C + Size - 1,
    nth0(R, Grid, Row0),
    nth0(C, Row0, First),
    check_rows(Grid, R, R_end, C, C_end, First).

check_rows(_, I, R_end, _, _, _) :-
    I > R_end, !.
check_rows(Grid, I, R_end, C, C_end, First) :-
    check_cols(Grid, I, C, C_end, First),
    I1 is I + 1,
    check_rows(Grid, I1, R_end, C, C_end, First).

check_cols(_, _, J, C_end, _) :-
    J > C_end, !.
check_cols(Grid, I, J, C_end, First) :-
    nth0(I, Grid, Row),
    nth0(J, Row, First),
    J1 is J + 1,
    check_cols(Grid, I, J1, C_end, First).

% Recursive quadtree encoding
quadtree(Grid, R, C, Size, Result) :-
    ( same_region(Grid, R, C, Size) ->
        nth0(R, Grid, Row),
        nth0(C, Row, Char),
        Result = Char
    ; Half is Size // 2,
      quadtree(Grid, R, C, Half, TL),
      C_plus_half is C + Half,
      quadtree(Grid, R, C_plus_half, Half, TR),
      R_plus_half is R + Half,
      quadtree(Grid, R_plus_half, C, Half, BL),
      quadtree(Grid, R_plus_half, C_plus_half, Half, BR),
      atomic_list_concat(['(', TL, TR, BL, BR, ')'], Result)
    ).

% Read exactly N lines, converting each to a list of character atoms
read_lines(0, Acc, Grid) :-
    reverse(Acc, Grid).
read_lines(N, Acc, Grid) :-
    N > 0,
    read_line_to_string(user_input, Line),
    ( Line = end_of_file ->
        Grid = []
    ; clean_line(Line, Clean),
      string_chars(Clean, Chars),
      N1 is N - 1,
      read_lines(N1, [Chars|Acc], Grid)
    ).

main :-
    read_line_to_string(user_input, Line1),
    ( Line1 = end_of_file ->
        true
    ; clean_line(Line1, Clean1),
      number_string(N, Clean1),
      read_lines(N, [], Grid),
      quadtree(Grid, 0, 0, N, Result),
      write(Result),
      nl
    ).