module Main (main) where

import System.IO

solve :: [String] -> Int -> Int -> Int -> String
solve g r c s =
    let ch = (g !! r) !! c
        same = all (\i -> all (\j -> (g !! (r+i)) !! (c+j) == ch) [0..s-1]) [0..s-1]
    in if same then [ch]
       else let h = s `div` 2
            in "(" ++ solve g r c h ++ solve g r (c+h) h ++ solve g (r+h) c h ++ solve g (r+h) (c+h) h ++ ")"

main :: IO ()
main = do
    contents <- getContents
    let (nLine:rest) = lines contents
        n = read nLine :: Int
        g = take n rest
    putStrLn (solve g 0 0 n)