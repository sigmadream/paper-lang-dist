module Main where

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        [] -> return ()
        (n:rest) -> do
            let arr = take n rest
            if null arr
                then print 0
                else print (maxSubarray arr)

maxSubarray :: [Int] -> Int
maxSubarray (x:xs) = go x x xs
  where
    go best cur [] = best
    go best cur (y:ys) =
        let cur' = max y (cur + y)
            best' = max best cur'
        in go best' cur' ys
maxSubarray [] = 0