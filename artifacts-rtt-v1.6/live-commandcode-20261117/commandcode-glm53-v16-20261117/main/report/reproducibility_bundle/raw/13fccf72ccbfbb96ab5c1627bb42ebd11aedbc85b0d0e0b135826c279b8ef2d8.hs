module Main (main) where

main :: IO ()
main = do
  line <- getLine
  case map read (words line) :: [Integer] of
    [a, b] -> do
      let g = gcd a b
      putStrLn (show g)
      putStrLn (show ((a `div` g) * b))
    _ -> return ()