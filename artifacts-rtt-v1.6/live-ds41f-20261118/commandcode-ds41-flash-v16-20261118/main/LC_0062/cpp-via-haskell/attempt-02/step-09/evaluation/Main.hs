module Main where

choose :: Integer -> Integer -> Integer
choose n k
    | k < 0 || k > n = 0
    | otherwise = go 1 1
  where
    kk = min k (n - k)
    go i res
        | i > kk = res
        | otherwise = go (i + 1) (res * (n - kk + i) `div` i)

main :: IO ()
main = do
    input <- getContents
    case map read (words input) :: [Integer] of
        (m:n:_) -> print (choose (m + n - 2) (min (m - 1) (n - 1)))
        _ -> return ()