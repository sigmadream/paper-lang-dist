module Main (main) where

main :: IO ()
main = do
  inp <- getContents
  case map read (words inp) :: [Integer] of
    (a:b:_) -> do
      let g = gcd a b
      putStrLn (show g)
      putStrLn (show ((a `div` g) * b))
    _ -> return ()