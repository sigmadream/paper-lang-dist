module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Integer]
    case xs of
        [] -> return ()
        (n:rest) ->
            let vals = take (fromIntegral n) rest
            in if n == 0
               then putStrLn "0"
               else case vals of
                   [] -> putStrLn "0"
                   (v:vs) ->
                       let (_, best) = foldl' step (v, v) vs
                           step (cur, bestSoFar) x =
                               let cur' = max x (cur + x)
                                   best' = max bestSoFar cur'
                               in (cur', best')
                       in print best