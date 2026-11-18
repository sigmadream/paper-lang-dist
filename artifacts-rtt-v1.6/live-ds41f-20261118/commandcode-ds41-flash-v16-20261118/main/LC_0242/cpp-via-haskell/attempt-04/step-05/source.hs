module Main (main) where

import qualified Data.List as L

main :: IO ()
main = do
    input <- getContents
    case words input of
        (s:t:_) ->
            if length s == length t && L.sort s == L.sort t
                then putStrLn "1"
                else putStrLn "0"
        _ -> putStrLn "0"