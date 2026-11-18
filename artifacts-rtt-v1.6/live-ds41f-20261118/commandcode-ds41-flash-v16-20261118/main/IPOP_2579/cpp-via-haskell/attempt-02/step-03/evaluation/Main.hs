module Main where

main :: IO ()
main = do
    input <- getContents
    let values = map read (words input) :: [Int]
    case values of
        [] -> return ()
        (n:rest) -> do
            let scores = take n rest
                dp = 0 : build 1
                build i
                    | i > n = []
                    | i == 1 = scores !! 0 : build 2
                    | i == 2 =
                        let v = scores !! 0 + scores !! 1
                        in v : build 3
                    | otherwise =
                        let a = dp !! (i - 2)
                            b = dp !! (i - 3) + scores !! (i - 2)
                            v = max a b + scores !! (i - 1)
                        in v : build (i + 1)
            print (dp !! n)