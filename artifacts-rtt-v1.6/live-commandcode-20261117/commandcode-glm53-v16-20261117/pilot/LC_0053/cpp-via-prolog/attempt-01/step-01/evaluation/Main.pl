:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    current_input(In),
    read_line_to_codes(In, Line1),
    atom_codes(A1, Line1),
    atom_number(A1, N),
    read_line_to_codes(In, Line2),
    atom_codes(A2, Line2),
    atomic_list_parts(A2, Parts),
    maplist(atom_number, Parts, Nums),
    length(Nums, N),
    N > 0,
    Nums = [First|Rest],
    foldl(kadane, Rest, First-First, _-Best),
    write(Best), nl.

atomic_list_parts(A, Parts) :-
    atom_codes(A, Codes),
    split_codes(Codes, Parts).

split_codes(Codes, Parts) :-
    phrase(codes_parts(Parts), Codes).

codes_parts([P|Ps]) -->
    ws, {phrase(nonblank(P), Rest, Rest)}, !.
codes_parts([]) --> [].

ws --> [C], { C = 32 ; C = 9 ; C = 10 ; C = 13 }, ws.
ws --> [].

nonblank([C|Cs]) --> [C], { C \= 32, C \= 9, C \= 10, C \= 13 }, nonblank(Cs).
nonblank([]) --> [].

kadale(_, _, _, _) :- fail.

kadane(X, Cur0-Best0, Cur-Best) :-
    Cur1 is max(X, Cur0 + X),
    Best is max(Best0, Cur1),
    Cur = Cur1.