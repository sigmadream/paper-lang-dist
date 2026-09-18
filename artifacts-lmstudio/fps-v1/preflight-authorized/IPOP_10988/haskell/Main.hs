palindrome [] = True
palindrome [_] = True
palindrome xs = head xs == last xs && palindrome (init (tail xs))
main = do
  s <- fmap (head . words) getContents
  print (if palindrome s then (1::Int) else 0)
