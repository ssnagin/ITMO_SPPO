package pokemons93055.pokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import pokemons93055.move.special.Confusion;
import pokemons93055.move.special.MagicalLeaf;
import pokemons93055.move.special.DazzlingGleam;
import pokemons93055.move.status.Swagger;

/**
 * Defines a new Pokemon - Celebi.
 * 
 * @author ssngn
 */
public class Celebi extends Pokemon {
    
    private final double HP = 310;
    private final double ATTACK = 184;
    private final double DEFENCE = 184;
    private final double SPECIAL_ATTACK = 184;
    private final double SPECIAL_DEFENCE = 184;
    private final double SPEED = 184;
    
    
    
    /**
     * 
     * @param name - Name of Celebi
     * @param level - initial level of pokemon
     */
    
    public Celebi(String name, int level) {
        
        super(name, level);
        
        setType(Type.PSYCHIC, Type.GRASS);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);
        
        setMove(new Confusion(), new MagicalLeaf(), new Swagger(), new DazzlingGleam());
        
    }
    
    
    
}
