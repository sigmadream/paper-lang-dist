module Main (main) where

import Data.Char (ord)
import qualified Data.Map.Strict as M

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  let f = M.fromListWith (+) . map (\c -> (ord c, 1 :: Int))
  putStrLn (if f s == f t then "1" else "0")