:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
stairs([],_,Prev,One,Two,Best) :- Best is max(One,Two), Prev >= 0.
stairs([X|Xs],PrevBest,PrevScore,One,Two,Best) :-
    NewOne is PrevBest+X, NewTwo is One+X, Current is max(One,Two),
    stairs(Xs,Current,PrevScore,NewOne,NewTwo,Best).
main :- read_numbers([_|[A|Xs]]), stairs(Xs,0,A,A,A,Best), writeln(Best).
