module Main (main) where

import Data.Char (isDigit, isSpace)

main :: IO ()
main = do
  input <- getContents
  let n = read (takeWhile (\c -> isDigit c || c == '-') (dropWhile isSpace input)) :: Int
      counts = 0 : [ (counts !! (i `div` 2)) + (i `mod` 2) | i <- [1 .. n] ]
  putStrLn (unwords (map show counts))