:- use_module(library(readutil)).
:- use_module(library(write)).

main :-
    read_line_to_codes(user_input, Line1),
    atom_number(Line1, N),
    findall(Row, (between(1, N, _), read_line_to_codes(user_input, Row)), Rows),
    maplist(string_codes, Rows, Matrix),
    count_provinces(N, Matrix, Components),
    write(Components).

count_provinces(_, [], 0) :- !.
count_provinces(N, [Row|Rows], Components) :-
    findall(Col, (between(1, N, Col), nth0(Col-1, Row, 1)), Connected),
    length(Connected, Count),
    count_provinces(N, Rows, Remaining),
    Components is Count + Remaining.