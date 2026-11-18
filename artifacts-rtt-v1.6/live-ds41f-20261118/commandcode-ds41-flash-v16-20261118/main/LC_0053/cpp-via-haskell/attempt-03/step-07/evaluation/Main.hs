module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (t:ts) -> do
            let n = read t :: Int
                xs = map read (take n ts) :: [Integer]
            case xs of
                [] -> putStrLn "0"
                (x:rest) -> do
                    let (best, _) = foldl' step (x, x) rest
                    print best
  where
    step (best, cur) v =
        let cur' = max v (cur + v)
        in (max best cur', cur')