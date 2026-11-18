module Main where

main :: IO ()
main = do
  input <- getContents
  case words input of
    (mStr : nStr : _) ->
      let m = read mStr :: Int
          n = read nStr :: Int
          answer = last (foldl (\row _ -> scanl1 (+) row) (replicate n 1) [1 .. m - 1])
      in print answer
    _ -> return ()