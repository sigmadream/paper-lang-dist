module Main where

import Data.List (foldl')
import System.IO (hSetBuffering, stdout, BufferMode(..))

kadane :: [Integer] -> Integer
kadane [] = 0
kadane (x:xs) =
  let (_, best) = foldl' step (x, x) xs
  in best
  where
    step (cur, best) y =
      let cur' = max y (cur + y)
      in (cur', max best cur')

main :: IO ()
main = do
  hSetBuffering stdout LineBuffering
  input <- getContents
  let toks = words input
  case toks of
    [] -> return ()
    (nStr:_) -> do
      let n = read nStr :: Int
          xs = map read (take (max 0 n) (drop 1 toks)) :: [Integer]
      case xs of
        [] -> return ()
        _  -> print (kadane xs)