package pokemons93055.pokemons;

import ru.ifmo.se.pokemon.Type;
import pokemons93055.move.physical.Waterfall;


/**
 * Defines a new Pokemon - Bibarel.
 * 
 * @author ssngn
 */
public class Bibarel extends Bidoof {
    
    private final double HP = 268;
    private final double ATTACK = 157;
    private final double DEFENCE = 112;
    private final double SPECIAL_ATTACK = 103;
    private final double SPECIAL_DEFENCE = 112;
    private final double SPEED = 132;
    
    /**
     * 
     * @param name - Name of Bibarel
     * @param level - initial level of pokemon
     */
    
    public Bibarel(String name, int level) {
        super(name, level);
        
        setType(Type.NORMAL, Type.WATER);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);
        
        addMove(new Waterfall());   
    }
}
