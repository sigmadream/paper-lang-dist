:- module(main, [main/0]).
:- set_prolog_flag(verbose, silent).

main :-
    read_line_to(user_input, L1),
    ( L1 == end_of_file -> true
    ; atom_number(L1, N),
      read_line_to(user_input, L2),
      ( L2 == end_of_file -> M = 0
      ; atom_number(L2, M)
      ),
      read_edges(M, Edges),
      assertz(n(N)),
      forall(member(u(A,B), Edges),
             ( assertz(e(A,B)), assertz(e(B,A)) )),
      findall(V,
              ( between(1, N, V),
                V \= 1,
                ( e(1, V)
                ; e(1, W), e(W, V), W \= V
                ) ),
              Vs),
      sort(Vs, Sorted),
      length(Sorted, Ans),
      write(Ans), nl,
      retractall(e(_, _)),
      retractall(n(_))
    ),
    halt.

read_edges(0, []) :- !.
read_edges(M, [E|Es]) :-
    read_line_to(user_input, Line),
    ( Line == end_of_file -> E = u(0,0), Es = []
    ; split_string(Line, " ", " ", Parts),
      maplist(atom_number, Parts, [A, B]),
      E = u(A, B),
      M1 is M - 1,
      read_edges(M1, Es)
    ).