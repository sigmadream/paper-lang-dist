module Main where

main :: IO ()
main = do
  input <- getContents
  let (n:vals) = map read (words input) :: [Int]
      xs = take n vals
  case xs of
    [] -> putStrLn "0"
    (x:rest) -> print $ fst $ foldl step (x, x) rest
  where
    step (best, cur) v =
      let cur' = max v (cur + v)
      in (max best cur', cur')