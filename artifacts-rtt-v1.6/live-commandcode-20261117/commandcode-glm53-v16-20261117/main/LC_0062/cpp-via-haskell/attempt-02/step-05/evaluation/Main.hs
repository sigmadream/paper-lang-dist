module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getLine
  let ws = words inp
  case ws of
    (ms : ns : _) | Just m <- readMaybeInt ms, Just n <- readMaybeInt ns -> do
      let dp = iterate step (replicate (fromIntegral n) 1) !! (fromIntegral m - 1)
      print (last dp)
    _ -> return ()
  where
    step row = scanl1 (+) row

readMaybeInt :: String -> Maybe Integer
readMaybeInt s = case reads s of
  [(v, "")] -> Just v
  _         -> Nothing