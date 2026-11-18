import Data.List (sort)
frequencies [] = []
frequencies (x:xs) = let (same,rest) = span (==x) xs
                      in (x,1+length same) : frequencies rest
main = do
  [a,b] <- fmap words getContents
  print (if frequencies (sort a) == frequencies (sort b) then (1::Int) else 0)
