module Main where

import Data.Array (Array, elems, listArray, (!))
import Text.Read (readMaybe)

main :: IO ()
main = do
  input <- getContents
  let n0 = case words input of
             (x:_) -> maybe 0 id (readMaybe x)
             []    -> 0
      n = max 0 n0
      counts :: Array Int Int
      counts = listArray (0, n) [f i | i <- [0..n]]
      f 0 = 0
      f i = counts ! (i `div` 2) + (i `mod` 2)
  putStrLn . unwords . map show $ elems counts