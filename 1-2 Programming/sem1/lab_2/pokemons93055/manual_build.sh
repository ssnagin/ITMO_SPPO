javac -d target/ -cp lib/Pokemon.jar -sourcepath src/pokemons93055/Main.java
jar -cmf mf.mf Build.jar -C target/ . lib/Pokemon.jar
