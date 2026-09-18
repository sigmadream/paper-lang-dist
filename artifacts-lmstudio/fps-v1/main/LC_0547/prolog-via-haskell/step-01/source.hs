import Data.List (findIndex, isInfixOf)
import Data.Set (Set, empty, insert, member)

readNumbers :: IO [Int]
readNumbers = do
  line <- getLine
  return $ map read . words $ line

matrixRows :: Int -> [[Int]] -> [[Int]]
matrixRows n xs = take n (dropWhile null (iterate tail xs))

visit :: Set Int -> [[Int]] -> Set Int -> Set Int
visit seen rows todo =
  case findIndex (`member` seen) todo of
    Just i -> visit seen rows (todo \\ [i])
    Nothing ->
      let neighbors = concatMap (\(j, x) -> if x == 1 then [j] else []) (zip [0..] (rows !! head todo))
          newTodo = todo ++ filter (`notElem` seen) neighbors
      in visit (insert (head todo) seen) rows newTodo

components :: Int -> [[Int]] -> Set Int -> Int
components n rows seen = go 1
  where
    go i | i > n     = 0
         | member i seen = go (i + 1)
         | otherwise     = 1 + go (i + 1) `max` components' (i + 1)
    components' j | j > n     = 0
                  | member j seen = components' (j + 1)
                  | otherwise     = 1 + components' (j + 1)

main :: IO ()
main = do
  n <- length . head <$> readNumbers
  rows <- matrixRows n <$> replicateM n readNumbers
  let count = components n rows empty
  print count