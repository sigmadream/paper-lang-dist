module Main where

import qualified Data.Array as A

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        [] -> pure ()
        (n:rest) -> do
            let scores = take n rest
                scoreArr = A.listArray (1, n) scores :: A.Array Int Int
                dp = A.listArray (0, n) (0 : [val i | i <- [1..n]]) :: A.Array Int Int
                val 1 = scoreArr A.! 1
                val 2 = scoreArr A.! 1 + scoreArr A.! 2
                val i = max (dp A.! (i - 2)) (dp A.! (i - 3) + scoreArr A.! (i - 1)) + scoreArr A.! i
            print (dp A.! n)