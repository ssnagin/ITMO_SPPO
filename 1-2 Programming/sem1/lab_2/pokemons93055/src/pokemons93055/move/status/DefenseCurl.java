package pokemons93055.move.status;

import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Stat;

/**
 * Defines a new status - Defense Curl. It raises 
 * the user's Defense by one stage. Stats can be 
 * raised to a maximum of +6 stages each.
 * 
 * @author developer
 */
public class DefenseCurl extends StatusMove {
    
    private static final double POWER = 0;
    private static final double ACCURACY = 0;
    
    
    public DefenseCurl() {
        super(Type.NORMAL, POWER, ACCURACY);
    }
    
    @Override protected void applySelfEffects(Pokemon pokemon) {
        Effect effect = new Effect().stat(Stat.DEFENSE,
                (int) pokemon.getStat(Stat.DEFENSE) + 1);
        
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses Defence Curl!";
    }
}
