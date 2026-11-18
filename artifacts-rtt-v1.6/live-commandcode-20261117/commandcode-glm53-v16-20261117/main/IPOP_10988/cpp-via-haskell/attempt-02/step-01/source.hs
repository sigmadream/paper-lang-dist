module Main (main) where

import Data.Char (isSpace)

main :: IO ()
main = do
  inp <- getContents
  let s = takeWhile (not . isSpace) inp
  putStrLn $ if s == reverse s then "1" else "0"