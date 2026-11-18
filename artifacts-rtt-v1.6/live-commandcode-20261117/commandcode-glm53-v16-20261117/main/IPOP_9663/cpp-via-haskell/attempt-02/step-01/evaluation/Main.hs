module Main (main) where

import Data.IORef
import qualified Data.Vector.Mutable as V
import System.IO

main :: IO ()
main = do
    inp <- getContents
    let ns = words inp
    if null ns then return () else do
        let n = read (head ns) :: Int
        col <- V.replicate n False
        d1 <- V.replicate (2 * n - 1) False
        d2 <- V.replicate (2 * n - 1) False
        ans <- newIORef (0 :: Int)
        let solve r
                | r == n = modifyIORef' ans (+1)
                | otherwise = mapM_ try [0 .. n - 1]
                where
                    try c = do
                        let i1 = r + c
                            i2 = r - c + n - 1
                        cOk <- V.read col c
                        d1Ok <- V.read d1 i1
                        d2Ok <- V.read d2 i2
                        if cOk || d1Ok || d2Ok
                            then return ()
                            else do
                                V.write col c True
                                V.write d1 i1 True
                                V.write d2 i2 True
                                solve (r + 1)
                                V.write col c False
                                V.write d1 i1 False
                                V.write d2 i2 False
        solve 0
        a <- readIORef ans
        putStrLn (show a)