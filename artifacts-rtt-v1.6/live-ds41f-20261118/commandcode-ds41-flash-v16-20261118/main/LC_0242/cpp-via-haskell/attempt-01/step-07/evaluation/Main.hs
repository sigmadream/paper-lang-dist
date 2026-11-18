module Main (main) where

import Data.Char (ord)
import Data.Array (accumArray, elems)

main :: IO ()
main = do
    input <- getContents
    case words input of
        (s:t:_) -> putStrLn (if validAnagram s t then "1" else "0")
        _ -> return ()

validAnagram :: String -> String -> Bool
validAnagram s t
    | length s /= length t = False
    | otherwise = all (== 0) (elems counts)
  where
    counts = accumArray (+) 0 (0, 25)
        ( [(ord c - ord 'a', 1) | c <- s]
       ++ [(ord c - ord 'a', -1) | c <- t]
        )