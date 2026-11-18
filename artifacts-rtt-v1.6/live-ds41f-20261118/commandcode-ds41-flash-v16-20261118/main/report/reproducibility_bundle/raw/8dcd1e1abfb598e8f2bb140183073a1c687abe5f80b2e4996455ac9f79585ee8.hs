module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          xs = take n (map read rest :: [Int])
          nonzeros = filter (/= 0) xs
          result = nonzeros ++ replicate (n - length nonzeros) 0
      putStrLn (unwords (map show result))