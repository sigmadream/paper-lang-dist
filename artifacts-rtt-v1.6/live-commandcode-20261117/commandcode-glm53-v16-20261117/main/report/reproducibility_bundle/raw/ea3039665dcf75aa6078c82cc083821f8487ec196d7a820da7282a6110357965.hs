module Main (main) where

import Data.List (foldl')
import qualified Data.Map.Strict as M

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  let count = foldl' (\m c -> M.insertWith (+) c (1 :: Int) m) M.empty
      ok = count s == count t
  putStrLn (if ok then "1" else "0")