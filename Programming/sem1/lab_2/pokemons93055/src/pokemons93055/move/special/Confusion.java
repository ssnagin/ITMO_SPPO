package pokemons93055.move.special;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.SpecialMove;
import ru.ifmo.se.pokemon.Type;

import java.util.Random;

/**
 * Defines a new special move - Confusion. Confusion deals
 * damage and has a 10% chance of confusing target
 * 
 * Pokemons with the ability Own Tempo or 
 * those behind a Substitute cannot be confused
 * 
 * @author ssngn
 */
public class Confusion extends SpecialMove {
    
    private static final double POWER = 50;
    private static final double ACCURACY = 100;

    public Confusion() {
        super(Type.PSYCHIC, POWER, ACCURACY);
    }
    
    /**
     * 
     * @param pokemon
     */
    @Override protected void applyOppEffects(Pokemon pokemon) {
        Effect effect = new Effect().attack(1);
        
        // Generating random value from 0 to 1
        // if generated value less or equal 0.1, effect is applied:
        if (new Random().nextDouble() <= 0.1) {
            Effect.confuse(pokemon);
        }
        
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses Confusion!";
    }
}