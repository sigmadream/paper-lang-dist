import Data.List (sort)
duplicate (a:b:xs) = a == b || duplicate (b:xs)
duplicate _ = False
main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let xs = take (fromInteger (head values)) (tail values)
  print (if duplicate (sort xs) then (1::Int) else 0)
