package pokemons93055.move.physical;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Status;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new physical move - Double Hit. It
 * deals damage and will strike twice (with 35 base 
 * power each time).
 * 
 * In the case of a burn, the usual attack-halving still 
 * occurs so Facade hits with an effective power of 70.
 * 
 * @author developer
 */
public class DoubleHit extends PhysicalMove {
    
    private static final double POWER = 35;
    private static final double ACCURACY = 90;
    
    private static final int HITS = 2;
    private static final int PRIORITY = 0;

    
    public DoubleHit() {
        super(Type.NORMAL, POWER, ACCURACY, PRIORITY, HITS);
    }
    
    @Override protected String describe() {
        return "uses DoubleHit!";
    }
}
