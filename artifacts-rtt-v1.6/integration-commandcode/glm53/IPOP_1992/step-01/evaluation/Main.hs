module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size =
  let first = grid ! (r, c)
      same = all (\(i, j) -> grid ! (i, j) == first)
                 [(i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
  in if same
       then [first]
       else let h = size `div` 2
                tl = solve grid r c h
                tr = solve grid r (c + h) h
                bl = solve grid (r + h) c h
                br = solve grid (r + h) (c + h) h
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
  input <- getContents
  case lines input of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          gridRows = take n rest
          grid = listArray ((0, 0), (n - 1, n - 1))
                 [ (rows !! i) !! j | i <- [0 .. n - 1], j <- [0 .. n - 1] ]
          rows = map (\s -> s ++ repeat ' ') gridRows
      putStrLn (solve grid 0 0 n)