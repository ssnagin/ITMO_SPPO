javac -classpath lib/*:. -d target -sourcepath . src/pokemons93055/Main.java src/pokemons93055/pokemons/*.java src/pokemons93055/move/physical/*.java src/pokemons93055/move/status/*.java src/pokemons93055/move/special/*.java
jar -cvf mf.mf Build/Build.jar lib/* -C target/ .
