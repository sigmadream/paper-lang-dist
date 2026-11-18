module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) ->
      let n = read nStr :: Int
          xs = map read (take n rest) :: [Integer]
      in print (maxSubarray xs)

maxSubarray :: [Integer] -> Integer
maxSubarray [] = 0
maxSubarray (x:xs) = go xs x x
  where
    go [] _ best = best
    go (y:ys) cur best =
      let cur' = max y (cur + y)
          best' = max best cur'
      in go ys cur' best'