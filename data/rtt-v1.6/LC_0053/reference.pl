:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
kadane([],_,Best,Best).
kadane([X|Xs],Ending,Best,Answer) :- E is max(X,Ending+X), B is max(Best,E), kadane(Xs,E,B,Answer).
main :- read_numbers([_,X|Xs]), kadane(Xs,X,X,Answer), writeln(Answer).
