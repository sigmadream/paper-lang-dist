module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Integer]
    case nums of
        [] -> return ()
        (n : xs) ->
            let a = take (fromIntegral n) xs
            in case a of
                [] -> putStrLn "0"
                (x:rest) ->
                    let (_, best) = foldl' step (x, x) rest
                        step (cur, b) v =
                            let cur' = max v (cur + v)
                                b'   = max b cur'
                            in (cur', b')
                    in print best