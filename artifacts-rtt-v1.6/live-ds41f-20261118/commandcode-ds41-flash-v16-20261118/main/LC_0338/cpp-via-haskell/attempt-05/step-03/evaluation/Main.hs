module Main where

import Data.Array
import Text.Read (readMaybe)

main :: IO ()
main = do
  input <- getContents
  case readMaybe input :: Maybe Int of
    Nothing -> return ()
    Just n -> do
      let counts = array (0, n) ((0, 0) : [(i, counts ! (i `div` 2) + (i `mod` 2)) | i <- [1..n]]) :: Array Int Int
      putStrLn $ unwords [show (counts ! i) | i <- [0..n]]