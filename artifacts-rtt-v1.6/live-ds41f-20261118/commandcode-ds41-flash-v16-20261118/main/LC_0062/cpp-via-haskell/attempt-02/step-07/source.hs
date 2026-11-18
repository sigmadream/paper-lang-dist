module Main where

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Integer]
    case nums of
        (m:n:_) -> print (choose (m + n - 2) (min (m - 1) (n - 1)))
        _ -> return ()

choose :: Integer -> Integer -> Integer
choose n k
    | k < 0 = 0
    | otherwise = product [n - kk + 1 .. n] `div` product [1 .. kk]
  where
    kk = min k (n - k)