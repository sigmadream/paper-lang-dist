module Main (main) where

main :: IO ()
main = do
  line <- getLine
  let [a, b] = map read (words line) :: [Integer]
      g = gcd a b
  putStrLn (show g)
  putStrLn (show ((a `div` g) * b))