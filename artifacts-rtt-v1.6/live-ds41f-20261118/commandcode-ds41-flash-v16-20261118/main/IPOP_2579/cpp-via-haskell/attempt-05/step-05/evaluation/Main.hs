module Main where

main :: IO ()
main = do
    contents <- getContents
    let ws = words contents
    case ws of
        [] -> return ()
        (x:xs) -> do
            let n = read x :: Int
                scores = map read (take n xs) :: [Int]
                dp = 0 : map step [1..n]
                step 1 = scores !! 0
                step 2 = (scores !! 0) + (scores !! 1)
                step i = max (dp !! (i - 2)) ((dp !! (i - 3)) + (scores !! (i - 2))) + (scores !! (i - 1))
            putStrLn (show (dp !! n))