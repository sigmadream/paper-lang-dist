module Main where

import Data.Array

main :: IO ()
main = do
    contents <- getContents
    let nums = map read (words contents) :: [Int]
        n = head nums
        scoresList = take n (tail nums)
        score = listArray (1, n) scoresList :: Array Int Int
        dp = array (0, n)
            ( [(0, 0)]
           ++ [(1, score ! 1) | n >= 1]
           ++ [(2, score ! 1 + score ! 2) | n >= 2]
           ++ [(i, max (dp ! (i - 2)) (dp ! (i - 3) + score ! (i - 1)) + score ! i)
              | i <- [3..n]]
            )
    putStrLn (show (dp ! n))