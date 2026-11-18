module Main (main) where

import Data.Char (isAsciiLower)

main :: IO ()
main = do
  line <- getLine
  let s = takeWhile isAsciiLower line
  if null s
    then return ()
    else putStrLn (if s == reverse s then "1" else "0")