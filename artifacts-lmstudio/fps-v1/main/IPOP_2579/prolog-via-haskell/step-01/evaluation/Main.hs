import Data.List (foldl')

maxPoints :: [Int] -> Int
maxPoints xs = go 0 0 0 xs
  where
    go prevBest prevScore one two [] = max one two
    go prevBest prevScore one two (x:xs) =
      let newOne = prevBest + x
          newTwo = one + x
          current = max one two
      in go current prevScore newOne newTwo xs

main :: IO ()
main = do
  n <- readLn :: IO Int
  scores <- replicateM n readLn :: IO [Int]
  print $ maxPoints scores