module Main (main) where

import Data.Array

main :: IO ()
main = do
  inp <- getLine
  let n = maybe 0 id (readMaybeInt inp)
      counts = listArray (0, n) (0 : [ counts ! (i `div` 2) + (i `mod` 2) | i <- [1 .. n] ]) :: Array Integer Integer
      out = unwords [ show (counts ! i) | i <- [0 .. n] ]
  putStrLn out

readMaybeInt :: String -> Maybe Integer
readMaybeInt s =
  case words s of
    (x:_) | all (`elem` "-0123456789") x -> Just (read x)
    _ -> Nothing