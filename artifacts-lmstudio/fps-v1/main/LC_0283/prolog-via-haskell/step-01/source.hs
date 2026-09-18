import Data.List

main :: IO ()
main = do
  n <- readLn :: IO Int
  xs <- replicateM n readLn :: IO [Int]
  let (kept, zeroes) = partition (/= 0) xs
      out = kept ++ replicate (n - length kept) 0
  mapM_ print out