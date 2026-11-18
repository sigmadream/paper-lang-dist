module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  ms <- getLine
  mt <- getLine
  case (ms, mt) of
    (Just s, Just t) -> do
      if length s /= length t
        then putStrLn "0"
        else do
          let a = foldl' (\acc c -> inc acc c) (replicate 26 0) s
              b = foldl' (\acc c -> inc acc c) (replicate 26 0) t
          putStrLn (if a == b then "1" else "0")
    _ -> return ()
  where
    inc acc c = take i acc ++ [acc !! i + 1] ++ drop (i + 1) acc
      where i = fromEnum c - fromEnum 'a'