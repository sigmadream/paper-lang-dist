module Main where

import Data.List (sort)

main :: IO ()
main = do
    input <- getContents
    case words input of
        (s:t:_) ->
            if length s == length t && sort s == sort t
                then putStrLn "1"
                else putStrLn "0"
        _ -> putStrLn "0"