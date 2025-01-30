package pokemons93055.move.status;

import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Stat;

/**
 * Defines a new status - Swagger. It confuses 
 * the target and raises its Attack by two stages.
 * 
 * If one of the two effects cannot be invoked 
 * (for example the target is already confused or its 
 * Attack is already raised to the maximum of +6 stages), 
 * Swagger still works and will invoke the other effect.
 * 
 * Confused Pokémon have a 33% chance of hurting themselves 
 * each turn, for 1-4 attacking turns (50% chance in 
 * Generations 1-6). The damage received is as if the Pokémon 
 * attacks itself with a typeless 40 base power Physical attack.
 * 
 * @author developer
 */
public class Swagger extends StatusMove {
    
    private static final double POWER = 0;
    private static final double ACCURACY = 85;
    
    public Swagger() {
        super(Type.NORMAL, POWER, ACCURACY);
    }
    
    @Override protected void applySelfEffects(Pokemon pokemon) {
        Effect effect = new Effect().stat(Stat.ATTACK,
                (int) pokemon.getStat(Stat.ATTACK) + 2);
        
        Effect.confuse(pokemon);
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses Swagger!";
    }
}
