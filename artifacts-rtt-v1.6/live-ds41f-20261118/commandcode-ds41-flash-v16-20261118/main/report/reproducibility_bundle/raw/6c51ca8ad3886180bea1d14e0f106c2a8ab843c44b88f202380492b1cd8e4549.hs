module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                limit = max 0 n
                xs = map read (take limit rest) :: [Integer]
            case xs of
                [] -> return ()
                (x0 : xs') -> do
                    let step (cur, best) x =
                            let cur' = max x (cur + x)
                                best' = max best cur'
                            in (cur', best')
                        (_, best) = foldl' step (x0, x0) xs'
                    print best