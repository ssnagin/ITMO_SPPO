package pokemons93055.move.special;

import ru.ifmo.se.pokemon.SpecialMove;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

/**
 * Defines a new special move - MagicalLeaf. It deals damage 
 * and ignores changes to the Accuracy and Evasion stats. However, 
 * it will not hit Pokémon during the invulnerable stage of Bounce, 
 * Dig, Dive, Fly, Phantom Force, Shadow Force or Sky Drop.
 * 
 * @author ssngn
 */
public class MagicalLeaf extends SpecialMove {
    
    private static final double POWER = 60;
    private static final double ACCURACY = 100;

    public MagicalLeaf() {
        super(Type.GRASS, POWER, ACCURACY);
    }
    
    /**
     * 
     * @param pokemon 
     */
    @Override protected void applyOppEffects(Pokemon pokemon) {
        Effect effect = new Effect().attack(1);
        pokemon.addEffect(effect);
    }
    
    @Override protected String describe() {
        return "uses MagicalLeaf!";
    }
}
