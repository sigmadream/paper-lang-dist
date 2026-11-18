module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        [] -> return ()
        (n:rest) ->
            let vals = take n rest
            in case vals of
                [] -> return ()
                (x:xs) -> do
                    let (best, _) = foldl' step (x, x) xs
                        step (best, cur) v =
                            let cur' = max v (cur + v)
                                best' = max best cur'
                            in (best', cur')
                    print best