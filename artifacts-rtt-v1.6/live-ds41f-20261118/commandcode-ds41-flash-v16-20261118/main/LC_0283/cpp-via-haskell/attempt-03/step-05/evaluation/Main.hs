module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          vals = map read (take n rest) :: [Int]
          nonzeros = filter (/= 0) vals
          zeros = replicate (length vals - length nonzeros) 0
          result = nonzeros ++ zeros
      putStrLn (unwords (map show result))