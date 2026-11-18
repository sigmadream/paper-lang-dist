module Main (main) where

import System.IO

main :: IO ()
main = do
  hSetBuffering stdout LineBuffering
  input <- getContents
  case map (reads :: String -> [(Int, String)]) (words input) of
    ((a,_):rest) -> case rest of
      ((b,_):_) -> do
        let g = gcd a b
        print g
        print ((a `div` g) * b)
      _ -> return ()
    _ -> return ()