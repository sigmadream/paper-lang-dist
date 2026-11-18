module Main where

import Data.List (isInfixOf)

main :: IO ()
main = do
    input <- getContents
    case map read (words input) :: [Integer] of
        (a:b:_) -> do
            let g = gcd a b
            print g
            print ((a `div` g) * b)
        _ -> return ()