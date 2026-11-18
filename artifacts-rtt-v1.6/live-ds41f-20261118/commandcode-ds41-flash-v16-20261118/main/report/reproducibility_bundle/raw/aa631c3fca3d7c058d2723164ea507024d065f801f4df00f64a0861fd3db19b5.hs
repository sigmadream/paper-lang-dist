module Main where

main :: IO ()
main = do
  input <- getContents
  case words input of
    (mStr:nStr:_) -> do
      let m = read mStr :: Int
          n = read nStr :: Int
          row = foldl (\r _ -> scanl1 (+) r) (replicate n 1) [2..m]
      print (row !! (n - 1))
    _ -> return ()