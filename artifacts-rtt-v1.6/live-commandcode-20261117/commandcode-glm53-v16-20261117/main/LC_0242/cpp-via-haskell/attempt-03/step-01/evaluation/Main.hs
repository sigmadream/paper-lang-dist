module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  let counts = foldl' (\acc c -> acc ++ [fromEnum c - fromEnum 'a']) [] s
  let ok = length s == length t && go counts (map (\c -> fromEnum c - fromEnum 'a') t)
  putStrLn (if ok then "1" else "0")
  where
    go [] [] = True
    go (c:cs) (d:ds) = c == d && go cs ds
    go _ _ = False