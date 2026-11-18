module Main where

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n:rest) ->
      let scores = take n rest
          ans = solve n scores
      in print ans

solve :: Int -> [Int] -> Int
solve n scores
  | n <= 0 = 0
  | n == 1 = head scores
  | n == 2 = sum (take 2 scores)
  | otherwise = go 3 0 s0 (s0 + s1) s1 (drop 2 scores)
  where
    s0 = scores !! 0
    s1 = scores !! 1
    go _ _ _ d1 _ [] = d1
    go i d3 d2 d1 prev (s:rest) =
      let dCur = max d2 (d3 + prev) + s
      in go (i + 1) d2 d1 dCur s rest