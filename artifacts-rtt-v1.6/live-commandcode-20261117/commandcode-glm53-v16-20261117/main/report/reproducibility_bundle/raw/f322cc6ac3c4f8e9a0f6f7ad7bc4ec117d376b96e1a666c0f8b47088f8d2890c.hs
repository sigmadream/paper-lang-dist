module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  inp <- getContents
  let (nLine : rest) = lines inp
      n = read nLine :: Int
      xs = take n $ map read $ words $ unwords rest :: [Integer]
      nonZeros = filter (/= 0) xs
      zeros = filter (== 0) xs
  putStrLn $ intercalate " " (map show (nonZeros ++ zeros))