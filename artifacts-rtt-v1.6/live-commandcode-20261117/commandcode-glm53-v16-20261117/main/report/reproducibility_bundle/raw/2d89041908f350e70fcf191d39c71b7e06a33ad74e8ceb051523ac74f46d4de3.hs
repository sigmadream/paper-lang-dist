module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  inp <- getContents
  case words inp of
    (tok:_) -> do
      let n = read tok :: Int
          arr = 0 : [ (arr !! (i `div` 2)) + (i `mod` 2) | i <- [1..n] ]
      putStrLn (unwords (map show arr))
    _ -> return ()