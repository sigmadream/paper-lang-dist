module Main (main) where

import Data.Char (ord)
import qualified Data.Map.Strict as M
import Data.List (foldl')
import System.IO

counts :: String -> M.Map Char Int
counts = foldl' (\m c -> M.insertWith (+) c 1 m) M.empty

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  putStrLn $ if counts s == counts t then "1" else "0"