module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  case map read (words inp) :: [Integer] of
    []     -> return ()
    (n:xs) -> do
      let rest = take (fromIntegral n) xs
      case rest of
        [] -> return ()
        (y:ys) -> do
          let step (best, cur) x = (max best (cur + x), max x (cur + x))
              (best, _) = foldl' step (y, y) ys
          print best