module Main where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve arr r c size =
    let first = arr ! (r, c)
        same = all (\i -> all (\j -> arr ! (i, j) == first) [c .. c + size - 1])
                   [r .. r + size - 1]
    in if same
       then [first]
       else
           let half = size `div` 2
           in "(" ++ solve arr r c half
                  ++ solve arr r (c + half) half
                  ++ solve arr (r + half) c half
                  ++ solve arr (r + half) (c + half) half
                  ++ ")"

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (x:rest) -> do
            let n = read x :: Int
                rows = take n rest
                arr = listArray ((0, 0), (n - 1, n - 1)) (concat rows)
            putStrLn (solve arr 0 0 n)