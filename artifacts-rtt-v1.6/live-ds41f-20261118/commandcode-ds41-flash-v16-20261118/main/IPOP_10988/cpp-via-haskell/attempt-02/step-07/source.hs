module Main where

main :: IO ()
main = do
  s <- getLine
  let t = takeWhile (/= '\n') s
  putStrLn (if t == reverse t then "1" else "0")