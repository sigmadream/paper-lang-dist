module Main (main) where

gcd' :: Int -> Int -> Int
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
  inp <- getLine
  case map read (words inp) :: [Int] of
    [a, b] -> do
      let g = gcd' a b
      print g
      print ((a `div` g) * b)
    _ -> return ()