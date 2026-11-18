module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  case map (reads :: String -> [(Integer, String)]) (words inp) of
    ((nParsed, _):rest0) | [(n, "")] <- nParsed ->
      let xs = [v | ((v, "") : _) <- take (fromIntegral n) rest0]
      in if n < 1 || null xs
           then return ()
           else print (maxSubarray xs)
    _ -> return ()

maxSubarray :: [Integer] -> Integer
maxSubarray (x:xs) = fst $ foldl' step (x, x) xs
  where
    step (best, cur) v = let c = max v (cur + v) in (max best c, c)
maxSubarray [] = 0