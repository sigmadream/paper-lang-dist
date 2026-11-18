module Main where

main :: IO ()
main = do
    input <- getContents
    let values = map read (words input) :: [Integer]
    case values of
        (m : n : _) -> print (uniquePaths m n)
        _ -> return ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n = comb (m + n - 2) (min (m - 1) (n - 1))

comb :: Integer -> Integer -> Integer
comb n k =
    let k' = min k (n - k)
    in product [n - k' + 1 .. n] `div` product [1 .. k']