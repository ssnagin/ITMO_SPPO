/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package pokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Move;
import ru.ifmo.se.pokemon.Battle;



/**
 *
 * @author DEVELOPER
 */
public class Pokemons {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Pokemon pikapika = new Pokemon("Pikachu", 1);
        Pokemon chushka = new Pokemon("Chushka", 1);

        Battle testBattle = new Battle();
        
        testBattle.addAlly(pikapika);
        testBattle.addFoe(chushka);

        testBattle.go();
    }
}
