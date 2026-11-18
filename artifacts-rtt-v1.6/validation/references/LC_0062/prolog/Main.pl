:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
next_row([_|Xs],[1|Ys]) :- row_tail(Xs,1,Ys).
row_tail([],_,[]).
row_tail([X|Xs],Left,[Y|Ys]) :- Y is X+Left, row_tail(Xs,Y,Ys).
rows(1,Row,Row) :- !.
rows(M,Row,Out) :- next_row(Row,Next), K is M-1, rows(K,Next,Out).
main :- read_numbers([M,N]), length(First,N), maplist(=(1),First), rows(M,First,Last), last(Last,Answer), writeln(Answer).
