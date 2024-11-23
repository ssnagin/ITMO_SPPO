package pokemons93055.move.status;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new physical move - Focus Energy.
 * It increases critical hit ratio. 
 * 
 * @author developer
 */
public class FocusEnergy extends StatusMove {
    
    private static final double POWER = 0;
    private static final double ACCURACY = 0;
    
    public FocusEnergy() {
        super(Type.NORMAL, POWER, ACCURACY);
    }
    
    @Override protected String describe() {
        return "uses FocusEnergy!";
    }
}
