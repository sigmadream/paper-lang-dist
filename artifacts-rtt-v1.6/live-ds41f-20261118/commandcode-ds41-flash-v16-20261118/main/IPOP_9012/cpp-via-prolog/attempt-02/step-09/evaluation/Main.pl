:- use_module(library(readutil)).

main :-
    read_item(First),
    (   First == end_of_file
    ->  true
    ;   number_string(T, First),
        loop(T)
    ).

loop(0) :- !.
loop(N) :-
    read_item(Line),
    (   Line == end_of_file
    ->  true
    ;   (   valid(Line)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        loop(N1)
    ).

read_item(String) :-
    read_line_to_string(user_input, Raw),
    (   Raw == end_of_file
    ->  String = end_of_file
    ;   string_codes(Raw, Codes0),
        remove_cr(Codes0, Codes),
        string_codes(String, Codes)
    ).

remove_cr([], []).
remove_cr([13|T], R) :-
    !,
    remove_cr(T, R).
remove_cr([H|T], [H|R]) :-
    remove_cr(T, R).

valid(String) :-
    string_chars(String, Chars),
    balanced(Chars, 0).

balanced([], 0).
balanced(['('|Rest], Balance) :-
    Balance1 is Balance + 1,
    balanced(Rest, Balance1).
balanced([')'|Rest], Balance) :-
    Balance > 0,
    Balance1 is Balance - 1,
    balanced(Rest, Balance1).