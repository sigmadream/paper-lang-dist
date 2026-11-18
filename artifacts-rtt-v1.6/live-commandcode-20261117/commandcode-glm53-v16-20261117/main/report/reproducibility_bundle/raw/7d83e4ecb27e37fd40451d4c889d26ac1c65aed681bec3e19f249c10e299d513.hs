module Main (main) where

import Data.Char (ord)
import qualified Data.Map.Strict as M

main :: IO ()
main = do
  ms <- getLine
  mt <- getLine
  case (ms, mt) of
    (s, t) -> do
      let count = M.fromListWith (+) . map (\c -> (ord c - ord 'a', 1 :: Int))
          ok = length s == length t && count s == count t
      putStrLn (if ok then "1" else "0")