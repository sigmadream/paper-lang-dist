:- dynamic best/2.

main :-
    read_line_to_string(Input),
    string_splitter(Input, ' ', Values),
    maplist(string_number, Values, Numbers),
    nth0(0, Numbers, N),
    nth1(N, Numbers, Scores),
    initialize_best(N),
    calculate_best(Scores, N, BestScore),
    write(BestScore),
    nl.

string_number(String, Number) :-
    number_string(Number, String).

initialize_best(N) :-
    between(0, N, I),
    assertz(best(I, 0)).

calculate_best([], _, _).
calculate_best([S|Scores], N, BestScore) :-
    I is length(Scores) + 1,
    (I =:= 1 -> NewBest is S;
     I =:= 2 -> NewBest is S + nth0(0, Scores);
     true -> 
         best(I-2, Prev2),
         best(I-3, Prev3),
         NewBest is max(Prev2, Prev3 + nth0(I-2, Scores)) + S
    ),
    assertz(best(I, NewBest)),
    calculate_best(Scores, N, BestScore).

string_splitter([], _, []).
string_splitter([H|T], Delimiter, [Head|Tail]) :-
    H = Delimiter,
    string_splitter(T, Delimiter, Tail).
string_splitter([H|T], Delimiter, [Head|Tail]) :-
    not(H = Delimiter),
    append(Head, [H], NewHead),
    string_splitter(T, Delimiter, Tail).