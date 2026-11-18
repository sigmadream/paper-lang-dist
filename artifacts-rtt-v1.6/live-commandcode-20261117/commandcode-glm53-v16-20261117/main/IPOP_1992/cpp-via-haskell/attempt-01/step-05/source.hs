module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve g r c size =
    let first = g ! (r, c)
        same = all (\(i, j) -> g ! (i, j) == first)
              [ (i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    in if same
         then [first]
         else let h = size `div` 2
              in "(" ++ solve g r c h ++ solve g r (c + h) h
                     ++ solve g (r + h) c h ++ solve g (r + h) (c + h) h ++ ")"

main :: IO ()
main = do
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        rows = take n rest
        g = listArray ((0, 0), (n - 1, n - 1))
            [ rows !! i !! j | i <- [0 .. n - 1], j <- [0 .. n - 1] ] :: Array (Int, Int) Char
    putStrLn (solve g 0 0 n)