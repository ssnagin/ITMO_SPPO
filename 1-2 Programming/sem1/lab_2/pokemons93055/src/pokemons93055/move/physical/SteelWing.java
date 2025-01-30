package pokemons93055.move.physical;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new physical move - Steel Wing. It deals 
 * damage and has a 10% chance of raising the user's 
 * Defense by one stage.
 * 
 * @author developer
 */
public class SteelWing extends PhysicalMove {
    
    private static final double POWER = 70;
    private static final double ACCURACY = 90;
    
    public SteelWing() {
        super(Type.STEEL, POWER, ACCURACY);
    }
    
    @Override protected void applySelfEffects(Pokemon pokemon) {
        Effect effect = new Effect().chance(0.1).stat(Stat.DEFENSE,
                (int) pokemon.getStat(Stat.DEFENSE) + 1);
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses Steel Wing!";
    }
}
