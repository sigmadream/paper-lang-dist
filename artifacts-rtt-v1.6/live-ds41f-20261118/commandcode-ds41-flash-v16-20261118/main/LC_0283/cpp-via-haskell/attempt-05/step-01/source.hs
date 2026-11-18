module Main where

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Integer]
  case values of
    [] -> pure ()
    (n:rest) -> do
      let a = take (fromIntegral n) rest
          nonZeros = filter (/= 0) a
          zeros = replicate (length a - length nonZeros) 0
      putStrLn (unwords (map show (nonZeros ++ zeros)))