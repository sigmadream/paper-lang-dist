module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr:rest) ->
            case rest of
                [] -> putStrLn "0"
                (xStr:_) -> do
                    let n = read nStr :: Int
                        vals = map read (take n rest) :: [Integer]
                    case vals of
                        [] -> putStrLn "0"
                        (x:xs) -> do
                            let (_, best) = foldl' step (x, x) xs
                                step (cur, b) v =
                                    let nc = max v (cur + v)
                                    in (nc, max b nc)
                            print best