euclid a 0 = a
euclid a b = euclid b (a `mod` b)
main = do
  [a,b] <- fmap (map read . words) getContents :: IO [Integer]
  let g = euclid a b
  print g
  print ((a `div` g) * b)
