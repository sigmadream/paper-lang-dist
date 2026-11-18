module Main where

main :: IO ()
main = do
    input <- getContents
    let s = takeWhile (not . isSpace) input
    putStrLn (if s == reverse s then "1" else "0")
  where
    isSpace c = c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == '\f' || c == '\v'