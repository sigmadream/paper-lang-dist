main :-
    read_line(Codes),
    my_reverse(Codes, Rev),
    (   Codes == Rev
    ->  write(1)
    ;   write(0)
    ),
    nl.

read_line(Chars) :-
    get_char(C),
    (   C == end_of_file
    ->  Chars = []
    ;   C == '\n'
    ->  Chars = []
    ;   Chars = [C|Rest],
        read_line(Rest)
    ).

my_reverse(L, R) :-
    my_reverse(L, [], R).

my_reverse([], Acc, Acc).
my_reverse([H|T], Acc, R) :-
    my_reverse(T, [H|Acc], R).