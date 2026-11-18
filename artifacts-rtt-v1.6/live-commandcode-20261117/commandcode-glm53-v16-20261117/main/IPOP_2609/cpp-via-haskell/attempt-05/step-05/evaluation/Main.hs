module Main (main) where

main :: IO ()
main = do
  inp <- getLine
  let [a, b] = map read (words inp) :: [Integer]
      g = gcd a b
  putStrLn (show g)
  putStrLn (show (a `div` g * b))