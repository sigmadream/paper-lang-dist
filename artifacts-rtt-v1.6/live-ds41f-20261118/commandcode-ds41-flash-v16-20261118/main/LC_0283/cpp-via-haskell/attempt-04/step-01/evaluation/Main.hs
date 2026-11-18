module Main where

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Integer]
  case values of
    [] -> return ()
    (n:rest) -> do
      let arr = take (fromIntegral n) rest
          nonzero = filter (/= 0) arr
          zeroCount = length arr - length nonzero
          result = nonzero ++ replicate zeroCount 0
      putStrLn (unwords (map show result))