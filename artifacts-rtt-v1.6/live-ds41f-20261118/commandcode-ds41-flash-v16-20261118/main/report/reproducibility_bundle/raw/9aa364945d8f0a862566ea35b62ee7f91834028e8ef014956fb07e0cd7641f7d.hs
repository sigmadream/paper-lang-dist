module Main where

gcd' :: Integer -> Integer -> Integer
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
  input <- getContents
  case map read (words input) :: [Integer] of
    (a:b:_) -> do
      let g = gcd' a b
      putStrLn (show g)
      putStrLn (show ((a `div` g) * b))
    _ -> return ()