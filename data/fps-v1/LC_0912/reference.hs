merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys)
  | x <= y = x : merge xs (y:ys)
  | otherwise = y : merge (x:xs) ys
mergesort [] = []
mergesort [x] = [x]
mergesort xs = let (a,b) = splitAt (length xs `div` 2) xs
               in merge (mergesort a) (mergesort b)
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  putStrLn (unwords (map show (mergesort (take (head values) (tail values)))))
