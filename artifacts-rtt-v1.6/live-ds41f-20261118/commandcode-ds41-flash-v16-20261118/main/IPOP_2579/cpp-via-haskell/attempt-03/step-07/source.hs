module Main where

import Data.Array (Array, array, listArray, (!))

main :: IO ()
main = do
  input <- getContents
  let xs = map read (words input) :: [Int]
  case xs of
    [] -> return ()
    (n:rest) ->
      if n == 0
        then putStrLn "0"
        else do
          let a = listArray (1, n) (take n rest) :: Array Int Int
              dp = array (0, n) $
                    (0, 0) :
                    (if n >= 1 then [(1, a ! 1)] else []) ++
                    (if n >= 2 then [(2, a ! 1 + a ! 2)] else []) ++
                    [(i, max (dp ! (i - 2)) (dp ! (i - 3) + a ! (i - 1)) + a ! i)
                    | i <- [3 .. n]]
          print (dp ! n)