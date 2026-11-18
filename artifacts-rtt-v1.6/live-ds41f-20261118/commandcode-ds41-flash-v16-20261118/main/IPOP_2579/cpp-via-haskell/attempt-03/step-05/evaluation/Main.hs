module Main where

import Data.Array

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        [] -> return ()
        (n:rest) ->
            if n == 0
                then putStrLn "0"
                else do
                    let scores = take n rest
                        arr = listArray (1, n) scores :: Array Int Int
                        dp = listArray (0, n) [calc i | i <- [0..n]]
                        calc 0 = 0
                        calc 1 = arr ! 1
                        calc 2 = arr ! 1 + arr ! 2
                        calc i = max (dp ! (i - 2)) (dp ! (i - 3) + arr ! (i - 1)) + arr ! i
                    print (dp ! n)