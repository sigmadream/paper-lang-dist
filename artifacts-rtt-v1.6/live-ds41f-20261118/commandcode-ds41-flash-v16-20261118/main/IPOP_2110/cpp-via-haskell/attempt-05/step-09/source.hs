module Main where

import Data.List (sort)

countPlacements :: Integer -> [Integer] -> Integer
countPlacements _ [] = 0
countPlacements d (x:xs) = go 1 x xs
  where
    go cnt _ [] = cnt
    go cnt prev (y:ys)
      | y - prev >= d = go (cnt + 1) y ys
      | otherwise = go cnt prev ys

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (_n:cStr:rest) -> do
      let c = read cStr :: Integer
          homes = sort (map read rest :: [Integer])
          firstHome = head homes
          lastHome = last homes
          solve lo hi best
            | lo > hi = best
            | otherwise =
                let mid = lo + (hi - lo) `div` 2
                in if countPlacements mid homes >= c
                     then solve (mid + 1) hi mid
                     else solve lo (mid - 1) best
      print (solve 1 (lastHome - firstHome) 0)