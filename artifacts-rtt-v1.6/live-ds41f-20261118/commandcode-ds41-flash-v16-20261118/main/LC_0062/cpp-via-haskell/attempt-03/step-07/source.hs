module Main where

main :: IO ()
main = do
    input <- getContents
    case map read (words input) :: [Integer] of
        (m:n:_) -> print (uniquePaths (fromInteger m) (fromInteger n))
        _ -> return ()

uniquePaths :: Int -> Int -> Integer
uniquePaths m n =
    (iterate (scanl1 (+)) (replicate n 1) !! (m - 1)) !! (n - 1)