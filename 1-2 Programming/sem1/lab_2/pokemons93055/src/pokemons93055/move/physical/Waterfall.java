package pokemons93055.move.physical;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;

import java.util.Random;

/**
 * Defines a new physical move - Waterfall. It deals damage 
 * and has a 20% chance of causing the target to flinch 
 * (if the target has not yet moved).
 * 
 * @author developer
 */
public class Waterfall extends PhysicalMove {
    
    private static final double POWER = 80;
    private static final double ACCURACY = 100;
    
    public Waterfall() {
        super(Type.WATER, POWER, ACCURACY);
    }
    
    @Override protected void applyOppDamage(Pokemon pokemon, double damage) {

        if (new Random().nextDouble() <= 0.2) {
            Effect.flinch(pokemon);
        }
        pokemon.setMod(Stat.HP, (int) damage);
    }
    
    @Override protected String describe() {
        return "uses Waterfall!";
    }
}
