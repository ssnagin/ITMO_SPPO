package pokemons93055.move.status;

import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Stat;

/**
 * Defines a new status - Amnesia. It raises
 * the user's Special Defense by two stages.
 * 
 * @author developer
 */
public class Amnesia extends StatusMove {
    
    private static final double POWER = 0;
    private static final double ACCURACY = 0;
    
    public Amnesia() {
        super(Type.PSYCHIC, POWER, ACCURACY);
    }
    
    @Override protected void applySelfEffects(Pokemon pokemon) {
        Effect effect = new Effect().stat(Stat.SPECIAL_DEFENSE,
                (int) pokemon.getStat(Stat.SPECIAL_DEFENSE) + 1);
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses Amnesia!";
    }
}
