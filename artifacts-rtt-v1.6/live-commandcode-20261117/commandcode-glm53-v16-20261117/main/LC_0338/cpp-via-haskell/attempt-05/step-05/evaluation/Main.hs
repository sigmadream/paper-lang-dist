module Main (main) where

import Data.Char (isDigit, isSpace)
import Data.List (intercalate)

parseN :: String -> Int
parseN line =
  let (spaces, rest) = span isSpace line
      (sign, rest') = case rest of
        ('-':s) -> (-1, s)
        ('+':s) -> (1, s)
        s -> (1, s)
      (digits, _) = span isDigit rest'
      n = if null digits then 0 else sign * read digits
  in max 0 (min 100000 n)

main :: IO ()
main = do
  ml <- getLine
  let n = case ml of
        Just l -> parseN l
        Nothing -> 0
      counts = 0 : [ (counts !! (k `div` 2)) + (k `mod` 2) | k <- [1 .. n] ]
  putStrLn (intercalate " " (map show (take (n + 1) counts)))