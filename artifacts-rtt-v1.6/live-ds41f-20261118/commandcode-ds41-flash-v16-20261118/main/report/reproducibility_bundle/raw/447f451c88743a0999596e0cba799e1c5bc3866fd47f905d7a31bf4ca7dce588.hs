module Main where

main :: IO ()
main = do
  line <- getLine
  let s = takeWhile (/= ' ') line
  putStrLn (if s == reverse s then "1" else "0")