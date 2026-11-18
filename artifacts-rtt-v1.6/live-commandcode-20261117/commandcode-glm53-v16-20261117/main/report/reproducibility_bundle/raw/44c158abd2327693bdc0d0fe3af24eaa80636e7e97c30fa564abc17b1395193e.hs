module Main (main) where

import Data.Char (isLower)
import System.IO

main :: IO ()
main = do
  eof <- isEOF
  if eof
    then return ()
    else do
      line <- getLine
      let s = takeWhile isLower line
      if null s
        then return ()
        else do
          putStrLn (if s == reverse s then "1" else "0")