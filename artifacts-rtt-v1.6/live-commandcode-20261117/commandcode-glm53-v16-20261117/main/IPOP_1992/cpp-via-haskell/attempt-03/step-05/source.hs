module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve g r c s
    | same      = [ch]
    | otherwise = "(" ++ solve g r c h ++ solve g r (c+h) h ++ solve g (r+h) c h ++ solve g (r+h) (c+h) h ++ ")"
    where
        ch = g ! (r, c)
        h = s `div` 2
        same = all (\(i, j) -> g ! (r+i, c+j) == ch)
                   [ (i, j) | i <- [0 .. s-1], j <- [0 .. s-1] ]

main :: IO ()
main = do
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        g = listArray ((0, 0), (n-1, n-1))
            (concatMap (take n) (take n rest)) :: Array (Int, Int) Char
    putStrLn (solve g 0 0 n)