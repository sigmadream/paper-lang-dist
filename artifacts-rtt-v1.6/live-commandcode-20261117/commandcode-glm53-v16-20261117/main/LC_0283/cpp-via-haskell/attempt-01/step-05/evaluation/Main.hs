module Main (main) where

import System.Environment
import Data.List

main :: IO ()
main = do
  inp <- getContents
  let ws = words inp
  case ws of
    (nStr : rest) -> do
      let n = read nStr :: Int
          a = take n (map read rest :: [Integer])
          res = filter (/= 0) a ++ replicate (n - length (filter (/= 0) a)) 0
      putStrLn (intercalate " " (map show res))
    _ -> return ()