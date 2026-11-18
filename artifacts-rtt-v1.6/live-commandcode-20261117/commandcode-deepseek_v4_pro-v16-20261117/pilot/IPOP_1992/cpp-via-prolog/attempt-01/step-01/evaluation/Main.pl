:- module(main, [main/0]).

% Read N lines of codes and return a list of rows (each row is a list of character codes)
read_grid(0, []) :- !.
read_grid(K, [Row|Rows]) :-
    K > 0,
    read_line_to_codes(user_input, Row),
    K1 is K - 1,
    read_grid(K1, Rows).

% Check if the subgrid from (R,C) of size Size is uniform.
% If uniform, Code is the uniform character code.
is_uniform(Grid, R, C, Size, Code) :-
    nth0(R, Grid, Row0),
    nth0(C, Row0, Code),
    MaxR is R + Size - 1,
    MaxC is C + Size - 1,
    forall(
        (between(R, MaxR, I), between(C, MaxC, J)),
        (nth0(I, Grid, Row), nth0(J, Row, Code))
    ).

% Quad-tree encoding: returns a list of character codes.
quadtree(_, _, _, 0, _) :- !, fail.  % size should never be 0
quadtree(Grid, R, C, Size, Result) :-
    ( is_uniform(Grid, R, C, Size, Code) ->
        Result = [Code]
    ;
        Half is Size // 2,
        R1 is R + Half,
        C1 is C + Half,
        quadtree(Grid, R, C, Half, TL),
        quadtree(Grid, R, C1, Half, TR),
        quadtree(Grid, R1, C, Half, BL),
        quadtree(Grid, R1, C1, Half, BR),
        append([40|TL], TR, Temp1),
        append(Temp1, BL, Temp2),
        append(Temp2, BR, Temp3),
        append(Temp3, [41], Result)
    ).

main :-
    read_line_to_codes(user_input, FirstLine),
    ( FirstLine = [] -> halt ; true ),   % EOF guard
    number_codes(N, FirstLine),
    read_grid(N, Grid),
    quadtree(Grid, 0, 0, N, ResultCodes),
    atom_codes(ResultAtom, ResultCodes),
    write(ResultAtom),
    nl.