module Main (main) where

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
  let rows = take size (drop r grid)
      firstChar = (grid !! r) !! c
      subgrid = [take size (drop c row) | row <- rows]
      allSame = all (== firstChar) (concat subgrid)
  in if allSame
       then [firstChar]
       else
         let half = size `div` 2
         in "(" ++ solve grid r c half
               ++ solve grid r (c + half) half
               ++ solve grid (r + half) c half
               ++ solve grid (r + half) (c + half) half
               ++ ")"

main :: IO ()
main = do
  input <- getContents
  let ls = lines input
      result = case ls of
                 (nStr:_) ->
                   let n = read (takeWhile (/= ' ') nStr) :: Int
                       grid = take n (tail ls)
                   in solve grid 0 0 n
                 [] -> ""
  putStrLn result