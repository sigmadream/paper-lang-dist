module Main where

comb :: Integer -> Integer -> Integer
comb n k =
  let k' = min k (n - k)
      numerator = product [n - k' + 1 .. n]
      denominator = product [1 .. k']
  in numerator `div` denominator

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n = comb (m + n - 2) (min (m - 1) (n - 1))

main :: IO ()
main = do
  input <- getContents
  case words input of
    (m : n : _) -> print (uniquePaths (read m) (read n))
    _ -> return ()