module Main where

solve :: [[Char]] -> Int -> Int -> Int -> String
solve grid r c size
  | allSame = [first]
  | otherwise = "(" ++ solve grid r c half ++ solve grid r (c+half) half ++ solve grid (r+half) c half ++ solve grid (r+half) (c+half) half ++ ")"
  where
    first = grid !! r !! c
    half = size `div` 2
    allSame = all (== first) [grid !! i !! j | i <- [r .. r+size-1], j <- [c .. c+size-1]]

main :: IO ()
main = do
    inp <- getContents
    let ls = lines inp
    let n = read (head ls) :: Int
    let grid = take n (tail ls)
    putStrLn $ solve grid 0 0 n