:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, TLine),
    (   TLine == end_of_file
    ->  true
    ;   number_string(TLine, T),
        process(T)
    ).

process(0) :- !.
process(N) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   string_chars(Line, Chars),
        balanced(Chars, 0, Ok),
        (   Ok == true
        ->  write('YES'), nl
        ;   write('NO'), nl
        ),
        N1 is N - 1,
        process(N1)
    ).

balanced([], Balance, Ok) :-
    (   Balance =:= 0
    ->  Ok = true
    ;   Ok = false
    ).
balanced([C|Cs], Balance, Ok) :-
    (   C == '('
    ->  B1 is Balance + 1,
        balanced(Cs, B1, Ok)
    ;   C == ')'
    ->  (   Balance =:= 0
        ->  Ok = false
        ;   B1 is Balance - 1,
            balanced(Cs, B1, Ok)
        )
    ;   balanced(Cs, Balance, Ok)
    ).