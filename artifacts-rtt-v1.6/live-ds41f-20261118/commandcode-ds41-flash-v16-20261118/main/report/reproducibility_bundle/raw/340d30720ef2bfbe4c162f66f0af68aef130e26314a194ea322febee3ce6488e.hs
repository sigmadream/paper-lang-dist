module Main where

import Data.List (foldl')

step :: (Integer, Integer) -> Integer -> (Integer, Integer)
step (cur, best) x =
    let cur' = max x (cur + x)
        best' = max best cur'
    in (cur', best')

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nTok : rest) -> do
            let n = read nTok :: Int
                vals = take (max 0 n) (map (read :: String -> Integer) rest)
            case vals of
                [] -> putStrLn "0"
                (v : vs) ->
                    let (_, best) = foldl' step (v, v) vs
                    in print best