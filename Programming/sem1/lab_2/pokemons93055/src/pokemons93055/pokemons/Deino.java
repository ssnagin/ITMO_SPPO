package pokemons93055.pokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import pokemons93055.move.status.FocusEnergy;
import pokemons93055.move.status.Swagger;


/**
 * Defines a new Pokemon - Deino.
 * 
 * @author ssngn
 */
public class Deino extends Pokemon {
    
    private final double HP = 214;
    private final double ATTACK = 121;
    private final double DEFENCE = 94;
    private final double SPECIAL_ATTACK = 85;
    private final double SPECIAL_DEFENCE = 94;
    private final double SPEED = 72;
    
    /**
     * 
     * @param name - Name of Deino
     * @param level - initial level of pokemon
     */
    
    public Deino(String name, int level) {
        super(name, level);
        
        setType(Type.DARK, Type.DRAGON);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);
        
        setMove(new Swagger(), new FocusEnergy());   
    }
}
