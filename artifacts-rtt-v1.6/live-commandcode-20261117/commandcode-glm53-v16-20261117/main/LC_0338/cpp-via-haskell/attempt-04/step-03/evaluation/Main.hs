module Main (main) where

import Data.Array

main :: IO ()
main = do
  inp <- getContents
  let n = case reads (takeWhile (`notElem` "\r\n") (dropWhile (`elem` " \t") inp)) of
            [(v, _)] -> v
            _        -> 0 :: Int
      arr = listArray (0, n) (0 : [ arr ! (i `div` 2) + (i `mod` 2) | i <- [1 .. n] ]) :: Array Int Int
  putStrLn (unwords [ show (arr ! i) | i <- [0 .. n] ])