module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          xs = map read (take n rest) :: [Int]
          nonZeros = filter (/= 0) xs
          zeros = replicate (n - length nonZeros) 0
      putStrLn (unwords (map show (nonZeros ++ zeros)))