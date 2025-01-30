package pokemons93055.pokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import pokemons93055.move.physical.Facade;
import pokemons93055.move.status.Amnesia;
import pokemons93055.move.status.DefenseCurl;

/**
 * Defines a new Pokemon - Bidoof.
 * 
 * @author ssngn
 */
public class Bidoof extends Pokemon {
    
    private final double HP = 228;
    private final double ATTACK = 85;
    private final double DEFENCE = 76;
    private final double SPECIAL_ATTACK = 67;
    private final double SPECIAL_DEFENCE = 76;
    private final double SPEED = 60;
    
    /**
     * 
     * @param name - Name of Bidoof
     * @param level - initial level of pokemon
     */
    
    public Bidoof(String name, int level) {
        super(name, level);
        
        setType(Type.NORMAL);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);
        
        setMove(new Facade(), new Amnesia(), new DefenseCurl());   
    }
}
