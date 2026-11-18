module Main where

comb :: Integer -> Integer -> Integer
comb n k
    | k < 0 || k > n = 0
    | otherwise = foldl step 1 [1 .. kk]
  where
    kk = min k (n - k)
    step acc i = (acc * (n - kk + i)) `div` i

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n = comb (m + n - 2) (min (m - 1) (n - 1))

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Integer]
    case xs of
        (m : n : _) -> print (uniquePaths m n)
        _ -> return ()