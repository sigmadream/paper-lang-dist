import Data.List (foldl')
step (ending,best) x = let next = max x (ending+x)
                       in (next,max best next)
main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let xs = take (fromInteger (head values)) (tail values)
  print (snd (foldl' step (head xs,head xs) (tail xs)))
