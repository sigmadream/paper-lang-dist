module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nw : rest) -> do
      let n = read nw :: Int
          values = map read (take n rest) :: [Int]
          nonZeroes = filter (/= 0) values
          result = nonZeroes ++ replicate (n - length nonZeroes) 0
      putStrLn (unwords (map show result))