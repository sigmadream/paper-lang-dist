module Main where

main :: IO ()
main = interact $ \input ->
  let ls = lines input
      t = read (head ls) :: Int
      ss = take t (tail ls)
  in unlines (map check ss)

check :: String -> String
check s
  | go 0 s = "YES"
  | otherwise = "NO"
  where
    go :: Int -> String -> Bool
    go bal [] = bal == 0
    go bal ('(':xs) = go (bal + 1) xs
    go bal (')':xs)
      | bal == 0 = False
      | otherwise = go (bal - 1) xs
    go _ _ = False