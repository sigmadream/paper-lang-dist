module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          nums = map read (take n rest) :: [Integer]
          nonZero = filter (/= 0) nums
          zeros = replicate (n - length nonZero) 0
          result = nonZero ++ zeros
      putStrLn (unwords (map show result))