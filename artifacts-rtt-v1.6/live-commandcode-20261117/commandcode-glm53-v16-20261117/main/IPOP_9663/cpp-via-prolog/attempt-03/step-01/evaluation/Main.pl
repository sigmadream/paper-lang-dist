:- module(main, []).
:- set_prolog_flag(double_quotes, atom).

main :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> true
    ; number_codes(N, Cs),
      solve(0, N, _Cols, _D1, _D2, Ans),
      write(Ans), nl ).

solve(R, N, Cols, D1, D2, Ans) :-
    length(Cols, N),
    length(D1, L), L is 2*N-1,
    length(D2, L),
    maplist(=(0), Cols),
    maplist(=(0), D1),
    maplist(=(0), D2),
    count(0, R, N, Cols, D1, D2, 0, Ans).

count(R, R, _, _, _, _, A, A).
count(R, N, Cols, D1, D2, _, A0, A) :-
    R < N,
    R1 is R+1,
    findall(t,
        ( between(0, N1, N1 is N-1),
          member(C, _),
          fail ), _) -> true ; true.