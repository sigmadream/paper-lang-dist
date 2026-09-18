:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
merge_lists([],B,B) :- !.
merge_lists(A,[],A) :- !.
merge_lists([A|As],[B|Bs],[A|Cs]) :- A =< B, !, merge_lists(As,[B|Bs],Cs).
merge_lists([A|As],[B|Bs],[B|Cs]) :- merge_lists([A|As],Bs,Cs).
merge_sort([],[]) :- !.
merge_sort([X],[X]) :- !.
merge_sort(Xs,Ys) :- length(Xs,N), H is N//2, length(A,H), append(A,B,Xs),
                    merge_sort(A,SA), merge_sort(B,SB), merge_lists(SA,SB,Ys).
main :- read_numbers([_|Xs]), merge_sort(Xs,Ys), write_numbers(Ys).
