module Main (main) where

import Data.Char (isSpace)

main :: IO ()
main = do
  s <- getContents
  let t = filter (\c -> c /= '\r' && not (isSpace c)) s
  putStrLn (if t == reverse t then "1" else "0")