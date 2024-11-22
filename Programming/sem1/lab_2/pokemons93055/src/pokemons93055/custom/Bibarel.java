/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package pokemons93055.custom;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

/**
 * 
 * @author developer
 */
public class Bibarel extends Pokemon {
    
    private final double HP = 310;
    private final double ATTACK = 184;
    private final double DEFENCE = 184;
    private final double SPECIAL_ATTACK = 184;
    private final double SPECIAL_DEFENCE = 184;
    private final double SPEED = 184;
            
    public Bibarel(String name, int level) {
        super(name, level);
        
        setType(Type.PSYCHIC, Type.GRASS);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);
        setMove();
        
    }
    
    
}
