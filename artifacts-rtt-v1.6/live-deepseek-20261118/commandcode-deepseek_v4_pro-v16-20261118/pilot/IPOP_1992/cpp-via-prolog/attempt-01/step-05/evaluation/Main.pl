remove_cr([], []).
remove_cr(Codes, Out) :-
    last(Codes, Last),
    (   Last =:= 13
    ->  length(Codes, Len),
        Len1 is Len - 1,
        length(Base, Len1),
        append(Base, [_], Codes),
        Out = Base
    ;   Out = Codes
    ).

all_same(Grid, R, C, Size, First) :-
    Rmax is R + Size - 1,
    Cmax is C + Size - 1,
    forall(
        ( between(R, Rmax, RR),
          between(C, Cmax, CC)
        ),
        ( nth0(RR, Grid, RowRR),
          nth0(CC, RowRR, Code),
          Code =:= First
        )
    ).

quadtree(_, R, C, 1, Result) :-
    !,
    nth0(R, Grid, Row),
    nth0(C, Row, Code),
    Result = [Code].
quadtree(Grid, R, C, Size, Result) :-
    nth0(R, Grid, Row),
    nth0(C, Row, First),
    (   all_same(Grid, R, C, Size, First)
    ->  Result = [First]
    ;   Half is Size // 2,
        R1 is R,
        C1 is C,
        R2 is R,
        C2 is C + Half,
        R3 is R + Half,
        C3 is C,
        R4 is R + Half,
        C4 is C + Half,
        quadtree(Grid, R1, C1, Half, TL),
        quadtree(Grid, R2, C2, Half, TR),
        quadtree(Grid, R3, C3, Half, BL),
        quadtree(Grid, R4, C4, Half, BR),
        append([TL, TR, BL, BR], Parts),
        append([[40], Parts, [41]], Result)
    ).

read_grid(0, Acc, Grid) :-
    reverse(Acc, Grid).
read_grid(N, Acc, Grid) :-
    N > 0,
    read_line_to_codes(user_input, Line),
    remove_cr(Line, CleanLine),
    N1 is N - 1,
    read_grid(N1, [CleanLine | Acc], Grid).

main :-
    read_line_to_codes(user_input, FirstLineCodes),
    (   FirstLineCodes = end_of_file
    ->  true
    ;   remove_cr(FirstLineCodes, CleanFirst),
        number_codes(N, CleanFirst),
        read_grid(N, [], Grid),
        quadtree(Grid, 0, 0, N, Result),
        format("~s~n", [Result])
    ).