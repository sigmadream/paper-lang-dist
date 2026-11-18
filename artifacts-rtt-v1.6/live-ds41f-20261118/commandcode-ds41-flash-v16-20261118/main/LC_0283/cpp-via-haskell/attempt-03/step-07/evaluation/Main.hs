module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nToken : rest) -> do
      let n = read nToken :: Int
          values = map read (take n rest) :: [Int]
          nonZero = filter (/= 0) values
          result = nonZero ++ replicate (n - length nonZero) 0
      putStrLn (unwords (map show result))