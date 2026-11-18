module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          xs = map read (take n rest) :: [Integer]
          nonZeros = filter (/= 0) xs
          zeros = filter (== 0) xs
          result = nonZeros ++ zeros
      putStrLn (unwords (map show result))