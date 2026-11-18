module Main where

main :: IO ()
main = do
  input <- getContents
  case words input of
    (mStr : nStr : _) -> do
      let m = read mStr :: Integer
          n = read nStr :: Integer
      print (uniquePaths m n)
    _ -> pure ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n =
  let k = min (m - 1) (n - 1)
      r = m + n - 2
      numerator = product [r - k + 1 .. r]
      denominator = product [1 .. k]
  in numerator `div` denominator