module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        [] -> pure ()
        (n:rest) -> putStrLn (show (solve n rest))

solve :: Int -> [Int] -> Int
solve n rest
    | n <= 0 = 0
    | n == 1 = case rest of
        (x:_) -> x
        _ -> 0
    | n == 2 = case rest of
        (x:y:_) -> x + y
        _ -> 0
    | otherwise = case take n rest of
        (s0:s1:remaining) ->
            let (_, _, d1, _) = foldl' step (0, s0, s0 + s1, s1) remaining
            in d1
        _ -> 0
  where
    step (d3, d2, d1, prev) s =
        let dCur = max d2 (d3 + prev) + s
        in (d2, d1, dCur, s)