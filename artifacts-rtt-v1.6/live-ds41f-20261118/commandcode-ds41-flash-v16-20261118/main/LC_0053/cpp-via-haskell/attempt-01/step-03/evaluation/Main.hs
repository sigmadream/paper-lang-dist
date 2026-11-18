module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr:rest) -> do
      let n = read nStr :: Int
          values = map read (take n rest) :: [Integer]
      if n == 0
        then putStrLn "0"
        else print (maxSubarray values)

maxSubarray :: [Integer] -> Integer
maxSubarray [] = 0
maxSubarray (x:xs) = go x x xs
  where
    go cur best [] = best
    go cur best (y:ys) =
      let cur' = max y (cur + y)
          best' = max best cur'
      in go cur' best' ys