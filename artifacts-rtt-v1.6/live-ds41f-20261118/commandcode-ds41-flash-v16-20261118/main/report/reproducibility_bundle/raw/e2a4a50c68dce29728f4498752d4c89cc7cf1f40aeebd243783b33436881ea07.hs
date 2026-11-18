module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nw:rest) -> do
            let n = read nw :: Int
                xs = take (max 0 n) (map read rest :: [Integer])
            case xs of
                [] -> return ()
                (x:xs') -> do
                    let (_, best) = foldl step (x, x) xs'
                        step (cur, best) y =
                            let cur' = max y (cur + y)
                                best' = max best cur'
                            in (cur', best')
                    print best