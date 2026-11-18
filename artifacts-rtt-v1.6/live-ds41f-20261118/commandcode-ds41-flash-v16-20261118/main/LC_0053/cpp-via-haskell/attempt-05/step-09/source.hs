module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
            if n <= 0
                then return ()
                else
                    let nums = map read (take n rest) :: [Integer]
                    in case nums of
                        [] -> return ()
                        (x:xs) -> do
                            let step (best, cur) v =
                                    let cur' = max v (cur + v)
                                    in (max best cur', cur')
                                (ans, _) = foldl' step (x, x) xs
                            print ans