module Main where

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n:rest) -> print (solve n (take n rest))

solve :: Int -> [Int] -> Int
solve n scores
  | n <= 0 = 0
  | n == 1 = s 1
  | n == 2 = s 1 + s 2
  | otherwise =
      let dp1 = s 1
          dp2 = dp1 + s 2
          (res, _, _) = foldl step (dp2, dp1, 0) [3..n]
      in res
  where
    s i = scores !! (i - 1)
    step (p1, p2, p3) i =
      let next = max p2 (p3 + s (i - 1)) + s i
      in (next, p1, p2)