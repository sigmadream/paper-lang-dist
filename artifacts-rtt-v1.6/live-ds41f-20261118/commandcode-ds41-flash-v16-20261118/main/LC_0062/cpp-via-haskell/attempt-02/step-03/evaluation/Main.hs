module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Integer]
    case nums of
        (m:n:_) -> print (uniquePaths m n)
        _ -> return ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n =
    let start = replicate (fromInteger n) 1
        final = foldl' (\dp _ -> scanl1 (+) dp) start [2..m]
    in last final