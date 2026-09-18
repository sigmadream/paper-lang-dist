import Data.List (sort)

main :: IO ()
main = do
    n <- readLn :: IO Int
    arr <- map read . words <$> getLine :: IO [Int]
    let sortedArr = sort arr
    putStrLn $ unwords (map show sortedArr)