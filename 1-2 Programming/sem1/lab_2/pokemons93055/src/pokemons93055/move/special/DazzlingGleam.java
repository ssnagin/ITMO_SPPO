package pokemons93055.move.special;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.SpecialMove;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new special move - Dazzling Gleam. It deals
 * damage and hits all adjacent opponents in double/triple battles.
 * 
 * @author developer
 */
public class DazzlingGleam extends SpecialMove {
    
    private static final double POWER = 80;
    private static final double ACCURACY = 100;
    
    private static final int HITS = 3;
    private static final int PRIORITY = 0;
    
    public DazzlingGleam() {
        super(Type.FAIRY, POWER, ACCURACY, PRIORITY, HITS);
    }
    
    @Override 
    protected String describe() {
        return "uses Dazzling Gleam!";
    }
}
