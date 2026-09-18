import Data.List (sort)

containsDuplicate :: [Int] -> Bool
containsDuplicate nums = any (uncurry (==)) $ zip nums (tail nums)

main :: IO ()
main = do
    n <- readLn :: IO Int
    nums <- replicateM n readLn :: IO [Int]
    if containsDuplicate nums then putStrLn "1" else putStrLn "0"