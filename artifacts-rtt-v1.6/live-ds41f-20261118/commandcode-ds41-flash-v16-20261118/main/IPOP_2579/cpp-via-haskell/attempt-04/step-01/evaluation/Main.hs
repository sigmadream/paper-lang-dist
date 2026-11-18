module Main where

main :: IO ()
main = do
  contents <- getContents
  let numbers = map read (words contents) :: [Int]
  case numbers of
    [] -> pure ()
    (n : rest) -> print (solve n rest)

solve :: Int -> [Int] -> Int
solve n xs =
  let scores = take n xs
  in case n of
       1 -> case scores of
              (s1 : _) -> s1
              _ -> 0
       2 -> case scores of
              (s1 : s2 : _) -> s1 + s2
              _ -> 0
       _ -> case scores of
              (s1 : s2 : remaining) ->
                let go a b c prev (x : more) =
                      let nxt = max b (a + prev) + x
                      in go b c nxt x more
                    go _ _ c _ [] = c
                in go 0 s1 (s1 + s2) s2 remaining
              _ -> 0