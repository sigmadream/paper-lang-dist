module Main where

import Data.Array (Array, (!), listArray)

main :: IO ()
main = do
  contents <- getContents
  let xs = map read (words contents) :: [Int]
  case xs of
    [] -> return ()
    (n:_) ->
      if n == 0
        then putStrLn "0"
        else do
          let sVals = take n (drop 1 xs ++ repeat 0)
              s :: Array Int Int
              s = listArray (1, n) sVals
          if n == 1
            then print (s ! 1)
            else do
              let initial = [0, s ! 1, s ! 1 + s ! 2]
                  build i dp
                    | i > n = dp
                    | otherwise =
                        let cur = max (dp !! (i - 2)) (dp !! (i - 3) + s ! (i - 1)) + s ! i
                        in build (i + 1) (dp ++ [cur])
                  dp = build 3 initial
              print (last dp)