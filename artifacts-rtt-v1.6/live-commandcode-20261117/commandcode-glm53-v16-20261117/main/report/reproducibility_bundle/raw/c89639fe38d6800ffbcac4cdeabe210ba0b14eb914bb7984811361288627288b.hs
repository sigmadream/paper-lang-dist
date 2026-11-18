module Main (main) where

main :: IO ()
main = do
  line <- getLine
  let t = takeWhile (\c -> c >= 'a' && c <= 'z') line
  putStrLn (if t == reverse t then "1" else "0")