module Main (main) where

import qualified Data.Map as M

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  let count = M.fromListWith (+) . map (\c -> (c, 1 :: Int))
  putStrLn $ if count s == count t then "1" else "0"