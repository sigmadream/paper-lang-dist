:- module(main, [main/0]).
:- dynamic edge/2.

main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; number_codes(N, L1),
      read_line_to_codes(user_input, L2),
      number_codes(M, L2),
      retractall(edge(_,_)),
      read_edges(M),
      findall(X, (edge(1,X), X \= 1), F1),
      findall(Y, (member(A,F1), edge(A,Y), Y \= 1, \+ member(Y,F1)), F2),
      length(F1, C1),
      length(F2, C2),
      Ans is C1 + C2,
      format("~d~n", [Ans]),
      main
    ).

read_edges(0) :- !.
read_edges(M) :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> true
    ; parse_pair(L, A, B),
      assertz(edge(A,B)),
      assertz(edge(B,A)),
      M1 is M - 1,
      read_edges(M1)
    ).

parse_pair(L, A, B) :-
    number_codes_skip(L, LA, R1),
    number_codes_skip(R1, LB, _),
    number_codes(A, LA),
    number_codes(B, LB).

number_codes_skip(L, A, R) :-
    append(A, R, L),
    A \= [],
    ( R == [] -> true ; R = [C|_], C == 32 ),
    catch(number_codes(_, A), _, fail).