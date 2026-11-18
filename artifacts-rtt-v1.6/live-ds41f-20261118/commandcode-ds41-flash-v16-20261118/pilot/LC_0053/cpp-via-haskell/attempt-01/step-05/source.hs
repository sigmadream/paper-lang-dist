module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                xs = map read (take n rest) :: [Int]
            if n == 0
                then return ()
                else print (maxSubArray xs)

maxSubArray :: [Int] -> Int
maxSubArray [] = 0
maxSubArray (x:xs) = snd (foldl' step (x, x) xs)
  where
    step (best, cur) v =
        let cur' = max v (cur + v)
            best' = max best cur'
        in (best', cur')