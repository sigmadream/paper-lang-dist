:- use_module(library(readutil)).
:- use_module(library(lists)).

main :-
    read_all_lines([], RevLines),
    reverse(RevLines, Lines),
    atomic_list_concat(Lines, ' ', Input),
    split_string(Input, " \t\n\r", " ", Tokens),
    maplist(token_to_number, Tokens, Nums),
    ( Nums = [N|Values], N > 0 ->
        take(N, Values, Selected),
        Selected = [First|Rest],
        max_subarray(Rest, First, First, Answer),
        writeln(Answer)
    ; true
    ).

read_all_lines(Acc, Lines) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Lines = Acc
    ; read_all_lines([Line|Acc], Lines)
    ).

token_to_number(Token, Number) :-
    number_string(Number, Token).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

max_subarray([], _, Best, Best) :- !.
max_subarray([X|Xs], Cur, Best, Answer) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best, Cur1),
    max_subarray(Xs, Cur1, Best1, Answer).